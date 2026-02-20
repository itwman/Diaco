"""
Diaco MES - Inventory Web Views (CRUD کامل)
=============================================
مدیریت موجودی الیاف، رنگ، مواد شیمیایی.
ورود/خروج با ثبت StockTransaction خودکار.
"""
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from apps.core.batch_utils import next_fiber_batch, jalali_today_display
from .models import FiberCategory, FiberStock, DyeStock, ChemicalStock, StockTransaction


# ══════════════════════════════════════════════════════════════
# ابزارها
# ══════════════════════════════════════════════════════════════

def _safe_decimal(val, default=None):
    if not val or str(val).strip() == '':
        return default
    try:
        return Decimal(str(val))
    except (InvalidOperation, ValueError):
        return default


# شماره‌گذاری از batch_utils مرکزی انجام می‌شود


def _record_transaction(stock_type, stock_id, txn_type, qty, unit, user, notes='', ref_type='', ref_id=None):
    """ثبت تراکنش انبار"""
    StockTransaction.objects.create(
        stock_type=stock_type,
        stock_id=stock_id,
        transaction_type=txn_type,
        quantity=qty,
        unit=unit,
        performed_by=user,
        notes=notes,
        reference_type=ref_type,
        reference_id=ref_id,
    )


# ══════════════════════════════════════════════════════════════
# موجودی الیاف
# ══════════════════════════════════════════════════════════════

@login_required
def fiber_list(request):
    """لیست موجودی الیاف + آمار + Modal ورود/خروج"""
    qs = FiberStock.objects.select_related('category').order_by('received_date')

    # فیلتر
    cat_id = request.GET.get('category', '')
    status_f = request.GET.get('status', '')
    grade_f = request.GET.get('grade', '')
    q = request.GET.get('q', '').strip()

    if cat_id:
        qs = qs.filter(category_id=cat_id)
    if status_f:
        qs = qs.filter(status=status_f)
    if grade_f:
        qs = qs.filter(quality_grade=grade_f)
    if q:
        qs = qs.filter(
            Q(batch_number__icontains=q) | Q(supplier__icontains=q) |
            Q(lot_number__icontains=q) | Q(warehouse_loc__icontains=q)
        )

    # آمار کلی
    available = FiberStock.objects.filter(status='available')
    stats = {
        'total_weight': available.aggregate(s=Sum('current_weight'))['s'] or Decimal('0'),
        'count_available': available.count(),
        'count_low': available.filter(current_weight__lt=100).count(),  # زیر ۱۰۰ kg هشدار
        'count_all': FiberStock.objects.count(),
    }

    return render(request, 'inventory/fiber_list.html', {
        'object_list': qs,
        'page_title': 'موجودی الیاف',
        'breadcrumb_parent': 'انبار',
        'categories': FiberCategory.objects.filter(is_active=True),
        'status_choices': FiberStock.Status.choices,
        'grade_choices': FiberStock.QualityGrade.choices,
        'cat_filter': cat_id,
        'status_filter': status_f,
        'grade_filter': grade_f,
        'search_query': q,
        'stats': stats,
        'suggested_batch': next_fiber_batch('FB'),  # نمونه — در Modal بر اساس دسته به‌روز می‌شود
        'today_jalali': jalali_today_display(),
    })


@login_required
@require_POST
def fiber_receive(request):
    """ورود الیاف به انبار — AJAX از Modal"""
    try:
        initial_weight = _safe_decimal(request.POST['initial_weight'])
        if not initial_weight or initial_weight <= 0:
            return JsonResponse({'ok': False, 'error': 'وزن باید بیشتر از صفر باشد'}, status=400)

        # پیشوند هوشمند بر اساس دسته انتخاب‌شده
        cat_code = ''
        try:
            from .models import FiberCategory
            cat_obj = FiberCategory.objects.get(pk=request.POST['category'])
            cat_code = cat_obj.code
        except Exception:
            pass
        batch_no = request.POST.get('batch_number', '').strip() or next_fiber_batch(cat_code)

        fiber = FiberStock.objects.create(
            category_id=request.POST['category'],
            batch_number=batch_no,
            lot_number=request.POST.get('lot_number', '').strip(),
            supplier=request.POST.get('supplier', '').strip(),
            color_raw=request.POST.get('color_raw', '').strip(),
            denier=_safe_decimal(request.POST.get('denier')),
            staple_length=_safe_decimal(request.POST.get('staple_length')),
            initial_weight=initial_weight,
            current_weight=initial_weight,  # ورود = موجودی کامل
            unit_price=_safe_decimal(request.POST.get('unit_price')),
            received_date=request.POST.get('received_date') or date.today(),
            expiry_date=request.POST.get('expiry_date') or None,
            warehouse_loc=request.POST.get('warehouse_loc', '').strip(),
            quality_grade=request.POST.get('quality_grade', 'A'),
            status='available',
            notes=request.POST.get('notes', '').strip(),
        )

        # ثبت تراکنش ورود
        _record_transaction(
            stock_type='fiber',
            stock_id=fiber.id,
            txn_type='receive',
            qty=initial_weight,
            unit='kg',
            user=request.user,
            notes=f"ورود اولیه — {fiber.supplier or 'بدون تأمین‌کننده'}",
        )

        return JsonResponse({
            'ok': True,
            'batch_number': fiber.batch_number,
            'weight': str(fiber.initial_weight),
            'message': f'الیاف بچ {fiber.batch_number} ({fiber.initial_weight} kg) وارد انبار شد',
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def fiber_issue(request, pk):
    """خروج/مصرف الیاف از انبار — AJAX"""
    fiber = get_object_or_404(FiberStock, pk=pk)
    try:
        qty = _safe_decimal(request.POST.get('quantity'))
        if not qty or qty <= 0:
            return JsonResponse({'ok': False, 'error': 'مقدار باید بیشتر از صفر باشد'}, status=400)
        if qty > fiber.current_weight:
            return JsonResponse({
                'ok': False,
                'error': f'موجودی کافی نیست. فقط {fiber.current_weight} kg موجود است'
            }, status=400)

        fiber.current_weight -= qty
        if fiber.current_weight == 0:
            fiber.status = 'consumed'
        fiber.save()

        _record_transaction(
            stock_type='fiber',
            stock_id=fiber.id,
            txn_type='issue',
            qty=qty,
            unit='kg',
            user=request.user,
            notes=request.POST.get('notes', '').strip(),
            ref_type=request.POST.get('ref_type', ''),
            ref_id=request.POST.get('ref_id') or None,
        )

        return JsonResponse({
            'ok': True,
            'remaining': str(fiber.current_weight),
            'status': fiber.status,
            'message': f'{qty} kg از بچ {fiber.batch_number} خارج شد. مانده: {fiber.current_weight} kg',
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def fiber_adjust(request, pk):
    """تعدیل موجودی — AJAX"""
    fiber = get_object_or_404(FiberStock, pk=pk)
    try:
        new_weight = _safe_decimal(request.POST.get('new_weight'))
        if new_weight is None or new_weight < 0:
            return JsonResponse({'ok': False, 'error': 'وزن نامعتبر'}, status=400)

        old_weight = fiber.current_weight
        diff = new_weight - old_weight
        fiber.current_weight = new_weight
        if new_weight == 0:
            fiber.status = 'consumed'
        elif fiber.status == 'consumed' and new_weight > 0:
            fiber.status = 'available'
        fiber.save()

        _record_transaction(
            stock_type='fiber',
            stock_id=fiber.id,
            txn_type='adjust',
            qty=abs(diff),
            unit='kg',
            user=request.user,
            notes=f"تعدیل: {old_weight} → {new_weight} kg | {request.POST.get('notes', '')}",
        )

        return JsonResponse({
            'ok': True,
            'new_weight': str(fiber.current_weight),
            'message': f'موجودی بچ {fiber.batch_number} به {new_weight} kg تعدیل شد',
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def fiber_get_json(request, pk):
    """دریافت اطلاعات یک بچ برای Modal"""
    fiber = get_object_or_404(FiberStock.objects.select_related('category'), pk=pk)
    return JsonResponse({
        'id': fiber.id,
        'batch_number': fiber.batch_number,
        'category_name': fiber.category.name,
        'supplier': fiber.supplier,
        'current_weight': str(fiber.current_weight),
        'initial_weight': str(fiber.initial_weight),
        'quality_grade': fiber.quality_grade,
        'warehouse_loc': fiber.warehouse_loc,
        'status': fiber.status,
        'status_display': fiber.get_status_display(),
    })


@login_required
def fiber_transactions(request, pk):
    """تاریخچه تراکنش‌های یک بچ"""
    fiber = get_object_or_404(FiberStock.objects.select_related('category'), pk=pk)
    transactions = StockTransaction.objects.filter(
        stock_type='fiber', stock_id=pk
    ).select_related('performed_by').order_by('-created_at')

    return render(request, 'inventory/fiber_transactions.html', {
        'fiber': fiber,
        'transactions': transactions,
        'page_title': f'تراکنش‌های {fiber.batch_number}',
        'breadcrumb_parent': 'انبار الیاف',
    })


# ══════════════════════════════════════════════════════════════
# موجودی رنگ (نمایش فعلی — CRUD بعدی)
# ══════════════════════════════════════════════════════════════

@login_required
def dye_list(request):
    qs = DyeStock.objects.all().order_by('-created_at')
    type_f = request.GET.get('type', '')
    status_f = request.GET.get('status', '')
    if type_f:
        qs = qs.filter(dye_type=type_f)
    if status_f:
        qs = qs.filter(status=status_f)
    return render(request, 'inventory/dye_list.html', {
        'object_list': qs,
        'page_title': 'موجودی رنگ',
        'breadcrumb_parent': 'انبار',
        'type_choices': DyeStock.DyeType.choices,
        'status_choices': DyeStock.Status.choices,
        'type_filter': type_f,
        'status_filter': status_f,
    })


@login_required
@require_POST
def dye_create(request):
    """ایجاد رنگ جدید"""
    try:
        initial = _safe_decimal(request.POST['initial'])
        DyeStock.objects.create(
            name=request.POST['name'].strip(),
            code=request.POST['code'].strip().upper(),
            dye_type=request.POST['type'],
            manufacturer=request.POST.get('mfr', '').strip(),
            batch_number=request.POST['batch'].strip(),
            initial_weight=initial,
            current_weight=_safe_decimal(request.POST.get('current')) or initial,
            unit=request.POST.get('unit', 'kg'),
            unit_price=_safe_decimal(request.POST.get('price')),
            received_date=request.POST.get('received') or date.today(),
            expiry_date=request.POST.get('expiry') or None,
            status=request.POST.get('status', 'available'),
            notes=request.POST.get('notes', '').strip(),
        )
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def dye_edit(request, pk):
    """ویرایش رنگ"""
    dye = get_object_or_404(DyeStock, pk=pk)
    try:
        dye.name = request.POST['name'].strip()
        dye.code = request.POST['code'].strip().upper()
        dye.dye_type = request.POST['type']
        dye.manufacturer = request.POST.get('mfr', '').strip()
        dye.batch_number = request.POST['batch'].strip()
        dye.current_weight = _safe_decimal(request.POST.get('current')) or dye.current_weight
        dye.unit = request.POST.get('unit', 'kg')
        dye.status = request.POST.get('status', 'available')
        dye.notes = request.POST.get('notes', '').strip()
        dye.save()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def chemical_list(request):
    qs = ChemicalStock.objects.all().order_by('-created_at')
    type_f = request.GET.get('type', '')
    status_f = request.GET.get('status', '')
    if type_f:
        qs = qs.filter(chemical_type=type_f)
    if status_f:
        qs = qs.filter(status=status_f)
    return render(request, 'inventory/chemical_list.html', {
        'object_list': qs,
        'page_title': 'مواد شیمیایی',
        'breadcrumb_parent': 'انبار',
        'type_choices': ChemicalStock.ChemicalType.choices,
        'status_choices': ChemicalStock.Status.choices,
        'type_filter': type_f,
        'status_filter': status_f,
    })


@login_required
@require_POST
def chemical_create(request):
    """ایجاد ماده شیمیایی"""
    try:
        initial = _safe_decimal(request.POST['initial'])
        ChemicalStock.objects.create(
            name=request.POST['name'].strip(),
            code=request.POST['code'].strip().upper(),
            chemical_type=request.POST['type'],
            manufacturer=request.POST.get('mfr', '').strip(),
            batch_number=request.POST['batch'].strip(),
            initial_amount=initial,
            current_amount=_safe_decimal(request.POST.get('current')) or initial,
            unit=request.POST.get('unit', 'kg'),
            concentration=_safe_decimal(request.POST.get('conc')),
            unit_price=_safe_decimal(request.POST.get('price')),
            received_date=request.POST.get('received') or date.today(),
            expiry_date=request.POST.get('expiry') or None,
            status=request.POST.get('status', 'available'),
            notes=request.POST.get('notes', '').strip(),
        )
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def chemical_edit(request, pk):
    """ویرایش ماده شیمیایی"""
    chem = get_object_or_404(ChemicalStock, pk=pk)
    try:
        chem.name = request.POST['name'].strip()
        chem.code = request.POST['code'].strip().upper()
        chem.chemical_type = request.POST['type']
        chem.manufacturer = request.POST.get('mfr', '').strip()
        chem.batch_number = request.POST['batch'].strip()
        chem.current_amount = _safe_decimal(request.POST.get('current')) or chem.current_amount
        chem.unit = request.POST.get('unit', 'kg')
        chem.concentration = _safe_decimal(request.POST.get('conc'))
        chem.status = request.POST.get('status', 'available')
        chem.notes = request.POST.get('notes', '').strip()
        chem.save()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)

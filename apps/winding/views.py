"""
Diaco MES - Winding Web Views (بوبین‌پیچی)
============================================
رابط وب برای مدیریت تولید بوبین‌پیچی.
list → create → detail → edit → status change
"""
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.core.models import Machine, Shift, ProductionLine
from apps.core.batch_utils import next_batch_number
from apps.spinning.models import Production as SpinningProduction
from apps.orders.models import Order
from .models import Production


def _safe_decimal(val, default=None):
    if val is None or str(val).strip() == '':
        return default
    try:
        return Decimal(str(val))
    except (InvalidOperation, ValueError):
        return default


def _safe_int(val, default=None):
    if val is None or str(val).strip() == '':
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# ══════════════════════════════════════════════════════════════
# لیست تولیدات
# ══════════════════════════════════════════════════════════════

@login_required
def production_list(request):
    """لیست تولیدات بوبین‌پیچی با فیلتر و آمار"""
    qs = Production.objects.select_related(
        'machine', 'operator', 'shift', 'order', 'spinning_production'
    ).order_by('-production_date', '-created_at')

    # فیلتر
    status_f = request.GET.get('status', '')
    machine_f = request.GET.get('machine', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    q = request.GET.get('q', '').strip()

    if status_f:
        qs = qs.filter(status=status_f)
    if machine_f:
        qs = qs.filter(machine_id=machine_f)
    if date_from:
        qs = qs.filter(production_date__gte=date_from)
    if date_to:
        qs = qs.filter(production_date__lte=date_to)
    if q:
        qs = qs.filter(
            Q(batch_number__icontains=q) |
            Q(order__order_number__icontains=q) |
            Q(machine__code__icontains=q)
        )

    # آمار
    stats = {
        'total': Production.objects.count(),
        'in_progress': Production.objects.filter(status='in_progress').count(),
        'completed': Production.objects.filter(status='completed').count(),
        'total_output_kg': Production.objects.filter(
            status='completed'
        ).aggregate(s=Sum('output_weight_kg'))['s'] or Decimal('0'),
    }

    return render(request, 'winding/list.html', {
        'object_list': qs,
        'page_title': 'تولید بوبین‌پیچی',
        'breadcrumb_parent': 'تکمیل نخ',
        'stats': stats,
        'machines': Machine.objects.filter(machine_type='winding', status='active'),
        'status_choices': Production.ProductionStatus.choices,
        'status_filter': status_f,
        'machine_filter': machine_f,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': q,
        'suggested_batch': next_batch_number('WD', Production),
    })


# ══════════════════════════════════════════════════════════════
# ایجاد تولید
# ══════════════════════════════════════════════════════════════

@login_required
def production_create(request):
    """فرم ایجاد بچ بوبین‌پیچی"""
    if request.method == 'POST':
        return _handle_create(request)

    return render(request, 'winding/form.html', {
        'page_title': 'ثبت بوبین‌پیچی جدید',
        'breadcrumb_parent': 'بوبین‌پیچی',
        'is_edit': False,
        'machines': Machine.objects.filter(machine_type='winding', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'spinning_batches': SpinningProduction.objects.filter(
            status='completed'
        ).order_by('-production_date')[:50],
        'suggested_batch': next_batch_number('WD', Production),
        'today': date.today().isoformat(),
        'package_choices': Production.PackageType.choices,
    })


def _handle_create(request):
    try:
        batch_number = request.POST.get('batch_number', '').strip() or next_batch_number('WD', Production)

        prod = Production.objects.create(
            batch_number=batch_number,
            machine_id=request.POST['machine'],
            operator=request.user,
            shift_id=request.POST['shift'],
            production_date=request.POST.get('production_date') or date.today(),
            production_line_id=request.POST.get('production_line') or None,
            order_id=request.POST.get('order') or None,
            spinning_production_id=request.POST.get('spinning_production') or None,
            # ورودی
            input_cops=_safe_int(request.POST.get('input_cops')),
            input_weight_kg=_safe_decimal(request.POST.get('input_weight_kg')),
            # پارامترها
            winding_speed_mpm=_safe_decimal(request.POST.get('winding_speed_mpm')),
            tension_setting_cn=_safe_decimal(request.POST.get('tension_setting_cn')),
            yarn_clearer_type=request.POST.get('yarn_clearer_type', '').strip(),
            # خروجی
            package_type=request.POST.get('package_type', 'cone'),
            package_weight_kg=_safe_decimal(request.POST.get('package_weight_kg')),
            output_packages=_safe_int(request.POST.get('output_packages')),
            output_weight_kg=_safe_decimal(request.POST.get('output_weight_kg')),
            waste_weight_kg=_safe_decimal(request.POST.get('waste_weight_kg')),
            # کیفیت
            cuts_per_100km=_safe_int(request.POST.get('cuts_per_100km')),
            splices_per_100km=_safe_int(request.POST.get('splices_per_100km')),
            efficiency_pct=_safe_decimal(request.POST.get('efficiency_pct')),
            notes=request.POST.get('notes', '').strip(),
        )
        return redirect('winding:detail', pk=prod.pk)
    except Exception as e:
        return render(request, 'winding/form.html', {
            'page_title': 'ثبت بوبین‌پیچی جدید',
            'breadcrumb_parent': 'بوبین‌پیچی',
            'is_edit': False,
            'error': str(e),
            'machines': Machine.objects.filter(machine_type='winding', status='active'),
            'shifts': Shift.objects.filter(is_active=True),
            'lines': ProductionLine.objects.filter(status='active'),
            'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
            'spinning_batches': SpinningProduction.objects.filter(status='completed').order_by('-production_date')[:50],
            'suggested_batch': next_batch_number('WD', Production),
            'today': date.today().isoformat(),
            'package_choices': Production.PackageType.choices,
            'post_data': request.POST,
        })


# ══════════════════════════════════════════════════════════════
# جزئیات بچ
# ══════════════════════════════════════════════════════════════

@login_required
def production_detail(request, pk):
    """صفحه جزئیات یک بچ بوبین‌پیچی"""
    prod = get_object_or_404(
        Production.objects.select_related(
            'machine', 'operator', 'shift', 'order', 'order__customer',
            'spinning_production', 'production_line'
        ),
        pk=pk
    )
    # بچ TFO مرتبط (اگر وجود دارد)
    tfo_batches = prod.tfo_productions.select_related('machine').all()

    return render(request, 'winding/detail.html', {
        'prod': prod,
        'tfo_batches': tfo_batches,
        'page_title': f'بوبین‌پیچی {prod.batch_number}',
        'breadcrumb_parent': 'بوبین‌پیچی',
    })


# ══════════════════════════════════════════════════════════════
# ویرایش
# ══════════════════════════════════════════════════════════════

@login_required
def production_edit(request, pk):
    """ویرایش یک بچ بوبین‌پیچی"""
    prod = get_object_or_404(Production, pk=pk)

    if request.method == 'POST':
        try:
            prod.machine_id = request.POST['machine']
            prod.shift_id = request.POST['shift']
            prod.production_date = request.POST.get('production_date') or prod.production_date
            prod.production_line_id = request.POST.get('production_line') or None
            prod.order_id = request.POST.get('order') or None
            prod.spinning_production_id = request.POST.get('spinning_production') or None
            prod.input_cops = _safe_int(request.POST.get('input_cops'))
            prod.input_weight_kg = _safe_decimal(request.POST.get('input_weight_kg'))
            prod.winding_speed_mpm = _safe_decimal(request.POST.get('winding_speed_mpm'))
            prod.tension_setting_cn = _safe_decimal(request.POST.get('tension_setting_cn'))
            prod.yarn_clearer_type = request.POST.get('yarn_clearer_type', '').strip()
            prod.package_type = request.POST.get('package_type', prod.package_type)
            prod.package_weight_kg = _safe_decimal(request.POST.get('package_weight_kg'))
            prod.output_packages = _safe_int(request.POST.get('output_packages'))
            prod.output_weight_kg = _safe_decimal(request.POST.get('output_weight_kg'))
            prod.waste_weight_kg = _safe_decimal(request.POST.get('waste_weight_kg'))
            prod.cuts_per_100km = _safe_int(request.POST.get('cuts_per_100km'))
            prod.splices_per_100km = _safe_int(request.POST.get('splices_per_100km'))
            prod.efficiency_pct = _safe_decimal(request.POST.get('efficiency_pct'))
            prod.notes = request.POST.get('notes', '').strip()
            prod.save()
            return redirect('winding:detail', pk=prod.pk)
        except Exception as e:
            pass

    return render(request, 'winding/form.html', {
        'page_title': f'ویرایش {prod.batch_number}',
        'breadcrumb_parent': 'بوبین‌پیچی',
        'is_edit': True,
        'prod': prod,
        'machines': Machine.objects.filter(machine_type='winding', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'spinning_batches': SpinningProduction.objects.filter(status='completed').order_by('-production_date')[:50],
        'package_choices': Production.PackageType.choices,
    })


# ══════════════════════════════════════════════════════════════
# تغییر وضعیت (AJAX)
# ══════════════════════════════════════════════════════════════

@login_required
@require_POST
def production_change_status(request, pk):
    """تغییر وضعیت یک بچ بوبین‌پیچی — AJAX"""
    prod = get_object_or_404(Production, pk=pk)
    new_status = request.POST.get('status')
    valid = [c[0] for c in Production.ProductionStatus.choices]
    if new_status not in valid:
        return JsonResponse({'ok': False, 'error': 'وضعیت نامعتبر'}, status=400)
    prod.status = new_status
    if new_status == 'completed' and not prod.completed_at:
        from datetime import datetime
        prod.completed_at = datetime.now()
    prod.save()
    return JsonResponse({
        'ok': True,
        'status': prod.status,
        'status_display': prod.get_status_display(),
        'message': f'وضعیت به «{prod.get_status_display()}» تغییر یافت',
    })

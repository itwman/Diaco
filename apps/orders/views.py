"""
Diaco MES - Orders Web Views (CRUD کامل)
==========================================
مشتریان، سفارشات، شیدهای رنگی.

رویکرد:
- مشتری: Modal (ساده) + صفحه جزئیات
- سفارش: صفحه جدا (پیچیده، فیلدهای زیاد)
- شید رنگی: Modal
"""
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.core.models import ProductionLine
from apps.core.batch_utils import next_order_number as _jalali_order_number
from .models import Customer, Order, ColorShade


# ══════════════════════════════════════════════════════════════
# ابزارها
# ══════════════════════════════════════════════════════════════

def _next_order_number():
    """شماره سفارش بعدی — تاریخ شمسی | مثال: ORD-040929-001"""
    return _jalali_order_number()


def _safe_decimal(val, default=None):
    if not val or str(val).strip() == '':
        return default
    try:
        return Decimal(str(val))
    except (InvalidOperation, ValueError):
        return default


# ══════════════════════════════════════════════════════════════
# مشتریان
# ══════════════════════════════════════════════════════════════

@login_required
def customer_list(request):
    """لیست مشتریان + Modal افزودن/ویرایش"""
    qs = Customer.objects.all().order_by('name')

    # جستجو
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(name__icontains=q) | Q(company__icontains=q) |
            Q(phone__icontains=q) | Q(city__icontains=q)
        )

    # فیلتر وضعیت
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        qs = qs.filter(is_active=True)
    elif status_filter == 'inactive':
        qs = qs.filter(is_active=False)

    return render(request, 'orders/customer_list.html', {
        'object_list': qs,
        'page_title': 'مشتریان',
        'breadcrumb_parent': 'سفارشات',
        'search_query': q,
        'status_filter': status_filter,
        'total_active': Customer.objects.filter(is_active=True).count(),
        'total_all': Customer.objects.count(),
    })


@login_required
@require_POST
def customer_create(request):
    """افزودن مشتری — AJAX از Modal"""
    try:
        customer = Customer.objects.create(
            name=request.POST['name'].strip(),
            company=request.POST.get('company', '').strip(),
            phone=request.POST.get('phone', '').strip(),
            mobile=request.POST.get('mobile', '').strip(),
            email=request.POST.get('email', '').strip(),
            city=request.POST.get('city', '').strip(),
            province=request.POST.get('province', '').strip(),
            address=request.POST.get('address', '').strip(),
            tax_id=request.POST.get('tax_id', '').strip(),
            credit_limit=_safe_decimal(request.POST.get('credit_limit')) or Decimal('0'),
            notes=request.POST.get('notes', '').strip(),
            is_active=True,
        )
        return JsonResponse({
            'ok': True,
            'id': customer.id,
            'name': str(customer),
            'message': f'مشتری «{customer.name}» ثبت شد',
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def customer_detail(request, pk):
    """جزئیات و ویرایش مشتری — صفحه کامل"""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            customer.name = request.POST['name'].strip()
            customer.company = request.POST.get('company', '').strip()
            customer.phone = request.POST.get('phone', '').strip()
            customer.mobile = request.POST.get('mobile', '').strip()
            customer.email = request.POST.get('email', '').strip()
            customer.city = request.POST.get('city', '').strip()
            customer.province = request.POST.get('province', '').strip()
            customer.address = request.POST.get('address', '').strip()
            customer.tax_id = request.POST.get('tax_id', '').strip()
            customer.credit_limit = _safe_decimal(request.POST.get('credit_limit')) or Decimal('0')
            customer.notes = request.POST.get('notes', '').strip()
            customer.is_active = request.POST.get('is_active') == 'on'
            customer.save()
            if is_ajax:
                return JsonResponse({'ok': True, 'message': f'«{customer.name}» بروزرسانی شد'})
            messages.success(request, f'اطلاعات «{customer.name}» بروزرسانی شد ✓')
            return redirect('orders:customer_detail', pk=customer.pk)
        except Exception as e:
            if is_ajax:
                return JsonResponse({'ok': False, 'error': str(e)}, status=400)
            messages.error(request, f'خطا: {e}')

    # سفارشات این مشتری
    orders = customer.orders.order_by('-created_at')[:10]
    return render(request, 'orders/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'page_title': customer.name,
        'breadcrumb_parent': 'مشتریان',
    })


@login_required
@require_POST
def customer_delete(request, pk):
    """حذف مشتری (غیرفعال‌سازی)"""
    customer = get_object_or_404(Customer, pk=pk)
    if customer.orders.filter(status__in=['confirmed', 'in_production']).exists():
        messages.error(request, 'این مشتری سفارش فعال دارد و قابل حذف نیست')
        return redirect('orders:customer_detail', pk=pk)
    customer.is_active = False
    customer.save()
    messages.success(request, f'مشتری «{customer.name}» غیرفعال شد')
    return redirect('orders:customer_list')


@login_required
def customer_get_json(request, pk):
    """دریافت اطلاعات مشتری برای Modal ویرایش"""
    customer = get_object_or_404(Customer, pk=pk)
    return JsonResponse({
        'id': customer.id,
        'name': customer.name,
        'company': customer.company,
        'phone': customer.phone,
        'mobile': customer.mobile,
        'email': customer.email,
        'city': customer.city,
        'province': customer.province,
        'address': customer.address,
        'tax_id': customer.tax_id,
        'credit_limit': str(customer.credit_limit),
        'notes': customer.notes,
        'is_active': customer.is_active,
    })


# ══════════════════════════════════════════════════════════════
# سفارشات
# ══════════════════════════════════════════════════════════════

@login_required
def order_list(request):
    """لیست سفارشات با فیلتر"""
    qs = Order.objects.select_related('customer', 'color_shade', 'production_line').order_by('-created_at')

    # جستجو
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(order_number__icontains=q) | Q(customer__name__icontains=q) |
            Q(yarn_type__icontains=q) | Q(yarn_count__icontains=q)
        )

    # فیلتر وضعیت
    status_f = request.GET.get('status', '')
    if status_f:
        qs = qs.filter(status=status_f)

    # فیلتر اولویت
    priority_f = request.GET.get('priority', '')
    if priority_f:
        qs = qs.filter(priority=priority_f)

    return render(request, 'orders/order_list.html', {
        'object_list': qs,
        'page_title': 'سفارشات',
        'breadcrumb_parent': 'سفارشات',
        'search_query': q,
        'status_filter': status_f,
        'priority_filter': priority_f,
        'status_choices': Order.Status.choices,
        'priority_choices': Order.Priority.choices,
        'customers': Customer.objects.filter(is_active=True).order_by('name'),
        'shades': ColorShade.objects.filter(is_approved=True).order_by('code'),
        # آمار سریع
        'count_in_production': Order.objects.filter(status='in_production').count(),
        'count_pending': Order.objects.filter(status__in=['draft', 'confirmed']).count(),
        'count_overdue': sum(1 for o in Order.objects.filter(
            status__in=['confirmed', 'in_production'],
            delivery_date__lt=date.today()
        )),
    })


@login_required
def order_create(request):
    """ایجاد سفارش جدید — صفحه کامل"""
    if request.method == 'POST':
        try:
            order = Order.objects.create(
                order_number=_next_order_number(),  # شمسی خودکار
                customer_id=request.POST['customer'],
                color_shade_id=request.POST.get('color_shade') or None,
                production_line_id=request.POST.get('production_line') or None,
                yarn_type=request.POST.get('yarn_type', '').strip(),
                yarn_count=request.POST.get('yarn_count', '').strip(),
                quantity_kg=_safe_decimal(request.POST['quantity_kg']),
                unit_price=_safe_decimal(request.POST.get('unit_price')),
                total_price=_safe_decimal(request.POST.get('total_price')),
                delivery_date=request.POST.get('delivery_date') or None,
                priority=request.POST.get('priority', 'normal'),
                status='draft',
                progress_pct=0,
                created_by=request.user,
                notes=request.POST.get('notes', '').strip(),
            )
            messages.success(request, f'سفارش {order.order_number} ایجاد شد ✓')
            return redirect('orders:order_detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'خطا در ثبت سفارش: {e}')

    return render(request, 'orders/order_form.html', {
        'page_title': 'سفارش جدید',
        'breadcrumb_parent': 'سفارشات',
        'is_create': True,
        'customers': Customer.objects.filter(is_active=True).order_by('name'),
        'shades': ColorShade.objects.filter(is_approved=True).order_by('code'),
        'lines': ProductionLine.objects.filter(status='active').order_by('code'),
        'status_choices': Order.Status.choices,
        'priority_choices': Order.Priority.choices,
    })


@login_required
def order_detail(request, pk):
    """جزئیات سفارش"""
    order = get_object_or_404(
        Order.objects.select_related('customer', 'color_shade', 'production_line', 'created_by'),
        pk=pk
    )
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'page_title': order.order_number,
        'breadcrumb_parent': 'سفارشات',
        'status_choices': Order.Status.choices,
    })


@login_required
def order_edit(request, pk):
    """ویرایش سفارش — صفحه کامل"""
    order = get_object_or_404(Order, pk=pk)

    if order.status in ('delivered', 'cancelled'):
        messages.warning(request, 'سفارش‌های تحویل‌شده یا لغوشده قابل ویرایش نیستند')
        return redirect('orders:order_detail', pk=pk)

    if request.method == 'POST':
        try:
            order.customer_id = request.POST['customer']
            order.color_shade_id = request.POST.get('color_shade') or None
            order.production_line_id = request.POST.get('production_line') or None
            order.yarn_type = request.POST.get('yarn_type', '').strip()
            order.yarn_count = request.POST.get('yarn_count', '').strip()
            order.quantity_kg = _safe_decimal(request.POST['quantity_kg'])
            order.unit_price = _safe_decimal(request.POST.get('unit_price'))
            order.total_price = _safe_decimal(request.POST.get('total_price'))
            order.delivery_date = request.POST.get('delivery_date') or None
            order.priority = request.POST.get('priority', 'normal')
            order.status = request.POST.get('status', order.status)
            order.progress_pct = int(request.POST.get('progress_pct', order.progress_pct))
            order.notes = request.POST.get('notes', '').strip()
            order.save()
            messages.success(request, f'سفارش {order.order_number} بروزرسانی شد ✓')
            return redirect('orders:order_detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'خطا: {e}')

    return render(request, 'orders/order_form.html', {
        'page_title': f'ویرایش {order.order_number}',
        'breadcrumb_parent': 'سفارشات',
        'is_create': False,
        'order': order,
        'customers': Customer.objects.filter(is_active=True).order_by('name'),
        'shades': ColorShade.objects.filter(is_approved=True).order_by('code'),
        'lines': ProductionLine.objects.filter(status='active').order_by('code'),
        'status_choices': Order.Status.choices,
        'priority_choices': Order.Priority.choices,
    })


@login_required
@require_POST
def order_change_status(request, pk):
    """تغییر وضعیت سفارش — POST → redirect (سازگار با USE_TZ=False)"""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    valid = [s[0] for s in Order.Status.choices]

    if new_status not in valid:
        messages.error(request, 'وضعیت نامعتبر')
        return redirect('orders:order_detail', pk=pk)

    # منطق کسب‌وکار: تأیید تولید فقط بعد از تأیید شید
    if new_status == 'in_production' and order.status not in ('confirmed', 'shade_approved'):
        messages.warning(request, 'برای شروع تولید ابتدا باید شید توسط مشتری تأیید شود')
        return redirect('orders:order_detail', pk=pk)

    order.status = new_status
    # پیشرفت خودکار بر اساس وضعیت
    progress_map = {
        'draft': 0,
        'shade_sent': 5,
        'shade_approved': 10,
        'confirmed': 15,
        'in_production': order.progress_pct or 20,  # حفظ پیشرفت فعلی
        'quality_check': 90,
        'ready': 95,
        'delivered': 100,
    }
    if new_status != 'in_production':  # in_production پیشرفت را ریست نکند
        order.progress_pct = progress_map.get(new_status, order.progress_pct)

    order.save()
    messages.success(request, f'وضعیت سفارش به «{order.get_status_display()}» تغییر یافت')
    return redirect('orders:order_detail', pk=pk)


@login_required
@require_POST
def order_cancel(request, pk):
    """لغو سفارش — AJAX یا form"""
    order = get_object_or_404(Order, pk=pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if order.status == 'in_production':
        err = 'سفارش در حال تولید است — ابتدا تولید را متوقف کنید'
        if is_ajax:
            return JsonResponse({'ok': False, 'error': err}, status=400)
        messages.error(request, err)
        return redirect('orders:order_detail', pk=pk)
    order.status = 'cancelled'
    order.save()
    if is_ajax:
        return JsonResponse({'ok': True, 'redirect': '/orders/'})
    messages.success(request, f'سفارش {order.order_number} لغو شد')
    return redirect('orders:order_list')


# ══════════════════════════════════════════════════════════════
# شیدهای رنگی
# ══════════════════════════════════════════════════════════════

@login_required
def shade_list(request):
    """لیست شیدهای رنگی + Modal افزودن"""
    qs = ColorShade.objects.order_by('code')
    return render(request, 'orders/shade_list.html', {
        'object_list': qs,
        'page_title': 'شیدهای رنگی',
        'breadcrumb_parent': 'سفارشات',
    })


@login_required
@require_POST
def shade_create(request):
    """افزودن شید — AJAX"""
    try:
        shade = ColorShade.objects.create(
            code=request.POST['code'].strip().upper(),
            name=request.POST['name'].strip(),
            color_hex=request.POST.get('color_hex', '').strip(),
            is_approved=request.POST.get('is_approved') == 'on',
            notes=request.POST.get('notes', '').strip(),
        )
        return JsonResponse({'ok': True, 'id': shade.id})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def shade_edit(request, pk):
    """ویرایش شید — AJAX"""
    shade = get_object_or_404(ColorShade, pk=pk)
    try:
        shade.code = request.POST['code'].strip().upper()
        shade.name = request.POST['name'].strip()
        shade.color_hex = request.POST.get('color_hex', '').strip()
        shade.is_approved = request.POST.get('is_approved') == 'on'
        shade.notes = request.POST.get('notes', '').strip()
        shade.save()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def shade_delete(request, pk):
    """حذف شید — AJAX"""
    shade = get_object_or_404(ColorShade, pk=pk)
    if shade.orders.exists():
        return JsonResponse({'ok': False, 'error': 'این شید در سفارش فعال استفاده شده و قابل حذف نیست'}, status=400)
    shade.delete()
    return JsonResponse({'ok': True})

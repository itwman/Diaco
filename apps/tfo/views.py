"""
Diaco MES - TFO Web Views (دولاتابی)
======================================
رابط وب برای مدیریت تولید دولاتابی TFO.
"""
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.core.models import Machine, Shift, ProductionLine
from apps.core.batch_utils import next_batch_number
from apps.winding.models import Production as WindingProduction
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
    """لیست تولیدات دولاتابی TFO"""
    qs = Production.objects.select_related(
        'machine', 'operator', 'shift', 'order', 'winding_production'
    ).order_by('-production_date', '-created_at')

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

    stats = {
        'total': Production.objects.count(),
        'in_progress': Production.objects.filter(status='in_progress').count(),
        'completed': Production.objects.filter(status='completed').count(),
        'total_output_kg': Production.objects.filter(
            status='completed'
        ).aggregate(s=Sum('output_weight_kg'))['s'] or Decimal('0'),
    }

    return render(request, 'tfo/list.html', {
        'object_list': qs,
        'page_title': 'تولید دولاتابی TFO',
        'breadcrumb_parent': 'تکمیل نخ',
        'stats': stats,
        'machines': Machine.objects.filter(machine_type='tfo', status='active'),
        'status_choices': Production.ProductionStatus.choices,
        'status_filter': status_f,
        'machine_filter': machine_f,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': q,
        'suggested_batch': next_batch_number('TFO', Production),
    })


# ══════════════════════════════════════════════════════════════
# ایجاد تولید
# ══════════════════════════════════════════════════════════════

@login_required
def production_create(request):
    if request.method == 'POST':
        return _handle_create(request)

    return render(request, 'tfo/form.html', {
        'page_title': 'ثبت دولاتابی TFO جدید',
        'breadcrumb_parent': 'دولاتابی TFO',
        'is_edit': False,
        'machines': Machine.objects.filter(machine_type='tfo', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'winding_batches': WindingProduction.objects.filter(
            status='completed'
        ).order_by('-production_date')[:50],
        'suggested_batch': next_batch_number('TFO', Production),
        'today': date.today().isoformat(),
        'twist_direction_choices': Production.TwistDirection.choices,
    })


def _handle_create(request):
    try:
        batch_number = request.POST.get('batch_number', '').strip() or next_batch_number('TFO', Production)
        prod = Production.objects.create(
            batch_number=batch_number,
            machine_id=request.POST['machine'],
            operator=request.user,
            shift_id=request.POST['shift'],
            production_date=request.POST.get('production_date') or date.today(),
            production_line_id=request.POST.get('production_line') or None,
            order_id=request.POST.get('order') or None,
            winding_production_id=request.POST.get('winding_production') or None,
            # مشخصات نخ
            ply_count=_safe_int(request.POST.get('ply_count')) or 2,
            input_yarn_count_ne=_safe_decimal(request.POST.get('input_yarn_count_ne')),
            output_yarn_count_ne=_safe_decimal(request.POST.get('output_yarn_count_ne')),
            # تاب
            twist_tpm=_safe_decimal(request.POST.get('twist_tpm')) or Decimal('0'),
            twist_direction=request.POST.get('twist_direction', 'S'),
            spindle_speed_rpm=_safe_int(request.POST.get('spindle_speed_rpm')),
            tension_weight_g=_safe_decimal(request.POST.get('tension_weight_g')),
            balloon_control=request.POST.get('balloon_control') == 'on',
            # تولید
            input_packages=_safe_int(request.POST.get('input_packages')),
            input_weight_kg=_safe_decimal(request.POST.get('input_weight_kg')),
            output_packages=_safe_int(request.POST.get('output_packages')),
            output_weight_kg=_safe_decimal(request.POST.get('output_weight_kg')),
            waste_weight_kg=_safe_decimal(request.POST.get('waste_weight_kg')),
            # کیفیت
            breakage_count=_safe_int(request.POST.get('breakage_count')) or 0,
            efficiency_pct=_safe_decimal(request.POST.get('efficiency_pct')),
            notes=request.POST.get('notes', '').strip(),
        )
        return redirect('tfo:detail', pk=prod.pk)
    except Exception as e:
        return render(request, 'tfo/form.html', {
            'page_title': 'ثبت دولاتابی TFO جدید',
            'breadcrumb_parent': 'دولاتابی TFO',
            'is_edit': False,
            'error': str(e),
            'machines': Machine.objects.filter(machine_type='tfo', status='active'),
            'shifts': Shift.objects.filter(is_active=True),
            'lines': ProductionLine.objects.filter(status='active'),
            'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
            'winding_batches': WindingProduction.objects.filter(status='completed').order_by('-production_date')[:50],
            'suggested_batch': next_batch_number('TFO', Production),
            'today': date.today().isoformat(),
            'twist_direction_choices': Production.TwistDirection.choices,
            'post_data': request.POST,
        })


# ══════════════════════════════════════════════════════════════
# جزئیات بچ
# ══════════════════════════════════════════════════════════════

@login_required
def production_detail(request, pk):
    prod = get_object_or_404(
        Production.objects.select_related(
            'machine', 'operator', 'shift', 'order', 'order__customer',
            'winding_production', 'production_line'
        ),
        pk=pk
    )
    heatset_batches = prod.heatset_batches.select_related('machine').all()

    return render(request, 'tfo/detail.html', {
        'prod': prod,
        'heatset_batches': heatset_batches,
        'page_title': f'دولاتابی {prod.batch_number}',
        'breadcrumb_parent': 'دولاتابی TFO',
    })


# ══════════════════════════════════════════════════════════════
# ویرایش
# ══════════════════════════════════════════════════════════════

@login_required
def production_edit(request, pk):
    prod = get_object_or_404(Production, pk=pk)

    if request.method == 'POST':
        try:
            prod.machine_id = request.POST['machine']
            prod.shift_id = request.POST['shift']
            prod.production_date = request.POST.get('production_date') or prod.production_date
            prod.production_line_id = request.POST.get('production_line') or None
            prod.order_id = request.POST.get('order') or None
            prod.winding_production_id = request.POST.get('winding_production') or None
            prod.ply_count = _safe_int(request.POST.get('ply_count')) or 2
            prod.input_yarn_count_ne = _safe_decimal(request.POST.get('input_yarn_count_ne'))
            prod.output_yarn_count_ne = _safe_decimal(request.POST.get('output_yarn_count_ne'))
            prod.twist_tpm = _safe_decimal(request.POST.get('twist_tpm')) or Decimal('0')
            prod.twist_direction = request.POST.get('twist_direction', prod.twist_direction)
            prod.spindle_speed_rpm = _safe_int(request.POST.get('spindle_speed_rpm'))
            prod.tension_weight_g = _safe_decimal(request.POST.get('tension_weight_g'))
            prod.balloon_control = request.POST.get('balloon_control') == 'on'
            prod.input_packages = _safe_int(request.POST.get('input_packages'))
            prod.input_weight_kg = _safe_decimal(request.POST.get('input_weight_kg'))
            prod.output_packages = _safe_int(request.POST.get('output_packages'))
            prod.output_weight_kg = _safe_decimal(request.POST.get('output_weight_kg'))
            prod.waste_weight_kg = _safe_decimal(request.POST.get('waste_weight_kg'))
            prod.breakage_count = _safe_int(request.POST.get('breakage_count')) or 0
            prod.efficiency_pct = _safe_decimal(request.POST.get('efficiency_pct'))
            prod.notes = request.POST.get('notes', '').strip()
            prod.save()
            return redirect('tfo:detail', pk=prod.pk)
        except Exception:
            pass

    return render(request, 'tfo/form.html', {
        'page_title': f'ویرایش {prod.batch_number}',
        'breadcrumb_parent': 'دولاتابی TFO',
        'is_edit': True,
        'prod': prod,
        'machines': Machine.objects.filter(machine_type='tfo', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'winding_batches': WindingProduction.objects.filter(status='completed').order_by('-production_date')[:50],
        'twist_direction_choices': Production.TwistDirection.choices,
    })


# ══════════════════════════════════════════════════════════════
# تغییر وضعیت (AJAX)
# ══════════════════════════════════════════════════════════════

@login_required
@require_POST
def production_change_status(request, pk):
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

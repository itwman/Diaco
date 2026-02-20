"""
Diaco MES - HeatSet Web Views (هیت‌ست / تثبیت حرارتی)
========================================================
رابط وب برای مدیریت بچ‌های هیت‌ست + لاگ چرخه دما/فشار.
"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.core.models import Machine, Shift, ProductionLine
from apps.core.batch_utils import next_batch_number
from apps.tfo.models import Production as TFOProduction
from apps.orders.models import Order
from .models import Batch, CycleLog


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
# لیست بچ‌ها
# ══════════════════════════════════════════════════════════════

@login_required
def batch_list(request):
    """لیست بچ‌های هیت‌ست"""
    qs = Batch.objects.select_related(
        'machine', 'operator', 'shift', 'order', 'tfo_production'
    ).order_by('-production_date', '-created_at')

    status_f = request.GET.get('status', '')
    machine_f = request.GET.get('machine', '')
    quality_f = request.GET.get('quality', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    q = request.GET.get('q', '').strip()

    if status_f:
        qs = qs.filter(status=status_f)
    if machine_f:
        qs = qs.filter(machine_id=machine_f)
    if quality_f:
        qs = qs.filter(quality_result=quality_f)
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

    completed = Batch.objects.filter(status='completed')
    stats = {
        'total': Batch.objects.count(),
        'processing': Batch.objects.filter(status__in=['loading', 'processing', 'cooling']).count(),
        'completed': completed.count(),
        'pass_count': completed.filter(quality_result='pass').count(),
        'fail_count': completed.filter(quality_result='fail').count(),
        'total_weight_kg': Batch.objects.aggregate(s=Sum('batch_weight_kg'))['s'] or Decimal('0'),
    }

    return render(request, 'heatset/list.html', {
        'object_list': qs,
        'page_title': 'هیت‌ست (تثبیت حرارتی)',
        'breadcrumb_parent': 'تکمیل نخ',
        'stats': stats,
        'machines': Machine.objects.filter(machine_type='heatset', status='active'),
        'status_choices': Batch.BatchStatus.choices,
        'quality_choices': Batch.QualityResult.choices,
        'status_filter': status_f,
        'machine_filter': machine_f,
        'quality_filter': quality_f,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': q,
        'suggested_batch': next_batch_number('HS', Batch),
    })


# ══════════════════════════════════════════════════════════════
# ایجاد بچ
# ══════════════════════════════════════════════════════════════

@login_required
def batch_create(request):
    if request.method == 'POST':
        return _handle_create(request)

    return render(request, 'heatset/form.html', {
        'page_title': 'ثبت بچ هیت‌ست جدید',
        'breadcrumb_parent': 'هیت‌ست',
        'is_edit': False,
        'machines': Machine.objects.filter(machine_type='heatset', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'tfo_batches': TFOProduction.objects.filter(status='completed').order_by('-production_date')[:50],
        'suggested_batch': next_batch_number('HS', Batch),
        'today': date.today().isoformat(),
        'machine_type_choices': Batch.MachineTypeHS.choices,
        'fiber_type_choices': Batch.FiberType.choices,
        'cycle_type_choices': Batch.CycleType.choices,
    })


def _handle_create(request):
    try:
        batch_number = request.POST.get('batch_number', '').strip() or next_batch_number('HS', Batch)
        batch = Batch.objects.create(
            batch_number=batch_number,
            machine_id=request.POST['machine'],
            operator=request.user,
            shift_id=request.POST['shift'],
            production_date=request.POST.get('production_date') or date.today(),
            production_line_id=request.POST.get('production_line') or None,
            order_id=request.POST.get('order') or None,
            tfo_production_id=request.POST.get('tfo_production') or None,
            # نوع فرآیند
            machine_type_hs=request.POST.get('machine_type_hs', 'autoclave'),
            fiber_type=request.POST.get('fiber_type', 'polyester'),
            cycle_type=request.POST.get('cycle_type', 'standard'),
            # پارامترهای حرارتی
            temperature_c=_safe_decimal(request.POST.get('temperature_c')) or Decimal('120'),
            steam_pressure_bar=_safe_decimal(request.POST.get('steam_pressure_bar')),
            vacuum_level_mbar=_safe_decimal(request.POST.get('vacuum_level_mbar')),
            humidity_pct=_safe_decimal(request.POST.get('humidity_pct')),
            # زمان‌بندی
            pre_heat_min=_safe_int(request.POST.get('pre_heat_min')),
            vacuum_time_min=_safe_int(request.POST.get('vacuum_time_min')),
            steam_time_min=_safe_int(request.POST.get('steam_time_min')),
            dwell_time_min=_safe_int(request.POST.get('dwell_time_min')),
            cooldown_min=_safe_int(request.POST.get('cooldown_min')),
            # بارگذاری
            batch_weight_kg=_safe_decimal(request.POST.get('batch_weight_kg')) or Decimal('0'),
            packages_count=_safe_int(request.POST.get('packages_count')),
            notes=request.POST.get('notes', '').strip(),
        )
        return redirect('heatset:detail', pk=batch.pk)
    except Exception as e:
        return render(request, 'heatset/form.html', {
            'page_title': 'ثبت بچ هیت‌ست جدید',
            'breadcrumb_parent': 'هیت‌ست',
            'is_edit': False,
            'error': str(e),
            'machines': Machine.objects.filter(machine_type='heatset', status='active'),
            'shifts': Shift.objects.filter(is_active=True),
            'lines': ProductionLine.objects.filter(status='active'),
            'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
            'tfo_batches': TFOProduction.objects.filter(status='completed').order_by('-production_date')[:50],
            'suggested_batch': next_batch_number('HS', Batch),
            'today': date.today().isoformat(),
            'machine_type_choices': Batch.MachineTypeHS.choices,
            'fiber_type_choices': Batch.FiberType.choices,
            'cycle_type_choices': Batch.CycleType.choices,
            'post_data': request.POST,
        })


# ══════════════════════════════════════════════════════════════
# جزئیات بچ
# ══════════════════════════════════════════════════════════════

@login_required
def batch_detail(request, pk):
    """صفحه جزئیات بچ هیت‌ست با نمودار چرخه دما/فشار"""
    batch = get_object_or_404(
        Batch.objects.select_related(
            'machine', 'operator', 'shift', 'order', 'order__customer',
            'tfo_production', 'production_line'
        ),
        pk=pk
    )
    cycle_logs = batch.cycle_logs.order_by('log_time')

    return render(request, 'heatset/detail.html', {
        'batch': batch,
        'cycle_logs': cycle_logs,
        'log_count': cycle_logs.count(),
        'page_title': f'هیت‌ست {batch.batch_number}',
        'breadcrumb_parent': 'هیت‌ست',
        'quality_choices': Batch.QualityResult.choices,
        'twist_stability_choices': Batch.TwistStability.choices,
        'status_choices': Batch.BatchStatus.choices,
        'phase_choices': CycleLog.Phase.choices,
    })


# ══════════════════════════════════════════════════════════════
# ویرایش
# ══════════════════════════════════════════════════════════════

@login_required
def batch_edit(request, pk):
    batch = get_object_or_404(Batch, pk=pk)

    if request.method == 'POST':
        try:
            batch.machine_id = request.POST['machine']
            batch.shift_id = request.POST['shift']
            batch.production_date = request.POST.get('production_date') or batch.production_date
            batch.production_line_id = request.POST.get('production_line') or None
            batch.order_id = request.POST.get('order') or None
            batch.tfo_production_id = request.POST.get('tfo_production') or None
            batch.machine_type_hs = request.POST.get('machine_type_hs', batch.machine_type_hs)
            batch.fiber_type = request.POST.get('fiber_type', batch.fiber_type)
            batch.cycle_type = request.POST.get('cycle_type', batch.cycle_type)
            batch.temperature_c = _safe_decimal(request.POST.get('temperature_c')) or batch.temperature_c
            batch.steam_pressure_bar = _safe_decimal(request.POST.get('steam_pressure_bar'))
            batch.vacuum_level_mbar = _safe_decimal(request.POST.get('vacuum_level_mbar'))
            batch.humidity_pct = _safe_decimal(request.POST.get('humidity_pct'))
            batch.pre_heat_min = _safe_int(request.POST.get('pre_heat_min'))
            batch.vacuum_time_min = _safe_int(request.POST.get('vacuum_time_min'))
            batch.steam_time_min = _safe_int(request.POST.get('steam_time_min'))
            batch.dwell_time_min = _safe_int(request.POST.get('dwell_time_min'))
            batch.cooldown_min = _safe_int(request.POST.get('cooldown_min'))
            batch.batch_weight_kg = _safe_decimal(request.POST.get('batch_weight_kg')) or batch.batch_weight_kg
            batch.packages_count = _safe_int(request.POST.get('packages_count'))
            # نتایج کیفی
            batch.quality_result = request.POST.get('quality_result') or None
            batch.shrinkage_pct = _safe_decimal(request.POST.get('shrinkage_pct'))
            batch.twist_stability = request.POST.get('twist_stability') or None
            batch.notes = request.POST.get('notes', '').strip()
            batch.save()
            return redirect('heatset:detail', pk=batch.pk)
        except Exception:
            pass

    return render(request, 'heatset/form.html', {
        'page_title': f'ویرایش {batch.batch_number}',
        'breadcrumb_parent': 'هیت‌ست',
        'is_edit': True,
        'batch': batch,
        'machines': Machine.objects.filter(machine_type='heatset', status='active'),
        'shifts': Shift.objects.filter(is_active=True),
        'lines': ProductionLine.objects.filter(status='active'),
        'orders': Order.objects.filter(status__in=['confirmed', 'in_production']).select_related('customer'),
        'tfo_batches': TFOProduction.objects.filter(status='completed').order_by('-production_date')[:50],
        'machine_type_choices': Batch.MachineTypeHS.choices,
        'fiber_type_choices': Batch.FiberType.choices,
        'cycle_type_choices': Batch.CycleType.choices,
        'quality_choices': Batch.QualityResult.choices,
        'twist_stability_choices': Batch.TwistStability.choices,
    })


# ══════════════════════════════════════════════════════════════
# تغییر وضعیت (AJAX)
# ══════════════════════════════════════════════════════════════

@login_required
@require_POST
def batch_change_status(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    new_status = request.POST.get('status')
    valid = [c[0] for c in Batch.BatchStatus.choices]
    if new_status not in valid:
        return JsonResponse({'ok': False, 'error': 'وضعیت نامعتبر'}, status=400)
    batch.status = new_status
    if new_status == 'processing' and not batch.started_at:
        batch.started_at = datetime.now()
    if new_status == 'completed' and not batch.completed_at:
        batch.completed_at = datetime.now()

    # نتایج کیفی همراه با تغییر وضعیت
    quality = request.POST.get('quality_result')
    if quality:
        batch.quality_result = quality
    shrinkage = request.POST.get('shrinkage_pct')
    if shrinkage:
        batch.shrinkage_pct = _safe_decimal(shrinkage)
    twist = request.POST.get('twist_stability')
    if twist:
        batch.twist_stability = twist

    batch.save()
    return JsonResponse({
        'ok': True,
        'status': batch.status,
        'status_display': batch.get_status_display(),
        'message': f'وضعیت به «{batch.get_status_display()}» تغییر یافت',
    })


# ══════════════════════════════════════════════════════════════
# ثبت لاگ چرخه (AJAX)
# ══════════════════════════════════════════════════════════════

@login_required
@require_POST
def cycle_log_add(request, pk):
    """ثبت لحظه‌ای دما/فشار/رطوبت در جدول CycleLog"""
    batch = get_object_or_404(Batch, pk=pk)
    try:
        log = CycleLog.objects.create(
            heatset_batch=batch,
            elapsed_min=_safe_decimal(request.POST.get('elapsed_min')),
            temperature_c=_safe_decimal(request.POST.get('temperature_c')),
            pressure_bar=_safe_decimal(request.POST.get('pressure_bar')),
            humidity_pct=_safe_decimal(request.POST.get('humidity_pct')),
            phase=request.POST.get('phase', 'steam'),
        )
        return JsonResponse({
            'ok': True,
            'id': log.id,
            'elapsed_min': str(log.elapsed_min or ''),
            'temperature_c': str(log.temperature_c or ''),
            'pressure_bar': str(log.pressure_bar or ''),
            'phase': log.phase,
            'phase_display': log.get_phase_display(),
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def cycle_log_data(request, pk):
    """دریافت داده‌های لاگ چرخه برای نمودار ApexCharts — JSON"""
    batch = get_object_or_404(Batch, pk=pk)
    logs = batch.cycle_logs.order_by('elapsed_min', 'log_time')

    data = {
        'elapsed': [],
        'temperature': [],
        'pressure': [],
        'humidity': [],
        'phases': [],
    }
    for log in logs:
        data['elapsed'].append(float(log.elapsed_min) if log.elapsed_min else None)
        data['temperature'].append(float(log.temperature_c) if log.temperature_c else None)
        data['pressure'].append(float(log.pressure_bar) if log.pressure_bar else None)
        data['humidity'].append(float(log.humidity_pct) if log.humidity_pct else None)
        data['phases'].append(log.get_phase_display())

    return JsonResponse(data)

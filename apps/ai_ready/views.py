"""
Diaco MES - AI Analytics API Views
=====================================
Endpointهای تحلیلی برای AI/ML.
"""
from datetime import date

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .utils import calculate_oee, get_timeseries_data, get_downtime_pattern
from apps.core.models import Machine


@login_required
def api_oee(request, machine_id):
    """OEE یک ماشین در تاریخ مشخص.
    GET /ai/oee/<machine_id>/?date=2026-02-16
    """
    target_date = request.GET.get('date')
    try:
        target_date = date.fromisoformat(target_date) if target_date else date.today()
    except ValueError:
        target_date = date.today()
    return JsonResponse(calculate_oee(machine_id, target_date))


@login_required
def api_oee_range(request, machine_id):
    """OEE محدوده‌ای برای نمودار.
    GET /ai/oee/<machine_id>/range/?days=30
    """
    from datetime import timedelta
    days = int(request.GET.get('days', 30))
    results = []
    for i in range(days):
        d = date.today() - timedelta(days=i)
        oee_data = calculate_oee(machine_id, d)
        results.append({
            'date': oee_data['date'],
            'oee': oee_data['oee'],
            'availability': oee_data['availability'],
            'performance': oee_data['performance'],
            'quality': oee_data['quality'],
        })
    results.reverse()
    return JsonResponse({'machine_id': machine_id, 'days': days, 'data': results})


@login_required
def api_timeseries(request, machine_id):
    """داده سری زمانی.
    GET /ai/timeseries/<machine_id>/?days=30&metric=output_weight
    """
    days = int(request.GET.get('days', 30))
    metric = request.GET.get('metric', 'output_weight')
    allowed = ['output_weight', 'efficiency_pct', 'breakage_count']
    if metric not in allowed:
        metric = 'output_weight'
    data = get_timeseries_data(machine_id, days, metric)
    return JsonResponse({'machine_id': machine_id, 'metric': metric, 'days': days, 'data': data})


@login_required
def api_downtime_pattern(request, machine_id):
    """الگوی توقفات (Predictive Maintenance).
    GET /ai/downtime-pattern/<machine_id>/?days=90
    """
    days = int(request.GET.get('days', 90))
    data = get_downtime_pattern(machine_id, days)
    return JsonResponse(data)


@login_required
def api_fleet_health(request):
    """سلامت کلی ماشین‌آلات.
    GET /ai/fleet-health/?line=1
    """
    machines = Machine.objects.filter(status='active')
    line_id = request.GET.get('line')
    if line_id:
        machines = machines.filter(production_line_id=line_id)
    results = []
    for m in machines:
        oee = calculate_oee(m.id)
        pattern = get_downtime_pattern(m.id, days=30)
        results.append({
            'machine_id': m.id,
            'code': m.code,
            'name': m.name,
            'section': m.get_machine_type_display(),
            'line': m.production_line.code if m.production_line else None,
            'oee_today': oee['oee'],
            'availability': oee['availability'],
            'risk_level': pattern['risk_level'],
            'mtbf_hours': pattern['mtbf_hours'],
            'failures_30d': pattern['total_failures'],
        })

    # مرتب‌سازی بر اساس ریسک
    risk_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    results.sort(key=lambda x: risk_order.get(x['risk_level'], 4))

    return JsonResponse({'machines': results, 'total': len(results)})

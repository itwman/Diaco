"""
Diaco MES - AI-Ready Utility Functions
=========================================
محاسبه OEE، استخراج داده سری زمانی، تحلیل الگو.
"""
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q

from apps.spinning.models import Production as SpinningProd
from apps.maintenance.models import DowntimeLog


def calculate_oee(machine_id, target_date=None):
    """
    محاسبه OEE (Overall Equipment Effectiveness) برای یک ماشین رینگ.

    OEE = Availability × Performance × Quality

    Availability = (Planned Time - Downtime) / Planned Time
    Performance  = efficiency_pct (از رکورد تولید)
    Quality      = 1 - (breakage_rate / threshold)

    Returns: dict با جزئیات OEE
    """
    if target_date is None:
        target_date = date.today()

    planned_minutes = 480  # ۸ ساعت = یک شیفت

    # توقفات روز
    downtime = DowntimeLog.objects.filter(
        machine_id=machine_id,
        start_time__date=target_date,
    ).aggregate(total=Sum('duration_min'))['total'] or 0

    availability = max(0, ((planned_minutes - downtime) / planned_minutes) * 100)

    # عملکرد (میانگین راندمان)
    spinning_qs = SpinningProd.objects.filter(
        machine_id=machine_id,
        production_date=target_date,
        status='completed',
    )
    perf_agg = spinning_qs.aggregate(
        avg_eff=Avg('efficiency_pct'),
        total_breakage=Sum('breakage_count'),
        total_spindles=Sum('num_spindles_active'),
    )

    performance = float(perf_agg['avg_eff'] or 0)

    # کیفیت (بر اساس نرخ پارگی)
    total_brk = perf_agg['total_breakage'] or 0
    total_sp = perf_agg['total_spindles'] or 1
    breakage_rate = (total_brk / total_sp) * 1000  # پارگی در هر ۱۰۰۰ دوک
    quality = max(0, min(100, 100 - breakage_rate))  # هر ۱ پارگی/۱۰۰۰ = ۱% کاهش

    oee = (availability * performance * quality) / 10000

    return {
        'machine_id': machine_id,
        'date': target_date.isoformat(),
        'availability': round(availability, 2),
        'performance': round(performance, 2),
        'quality': round(quality, 2),
        'oee': round(oee, 2),
        'downtime_min': downtime,
        'breakage_rate_per_1000': round(breakage_rate, 1),
        'batch_count': spinning_qs.count(),
    }


def get_timeseries_data(machine_id, days=30, metric='output_weight'):
    """
    استخراج داده سری زمانی برای یک ماشین.

    metric: output_weight | efficiency_pct | breakage_count
    Returns: list of {date, value}
    """
    start = date.today() - timedelta(days=days)
    qs = SpinningProd.objects.filter(
        machine_id=machine_id,
        production_date__gte=start,
        status='completed',
    ).values('production_date').annotate(
        value=Sum(metric) if metric != 'efficiency_pct' else Avg(metric),
    ).order_by('production_date')

    return [
        {'date': item['production_date'].isoformat(), 'value': float(item['value'] or 0)}
        for item in qs
    ]


def get_downtime_pattern(machine_id, days=90):
    """
    الگوی توقفات ماشین برای Predictive Maintenance.

    Returns: dict با تحلیل الگو
    """
    start = date.today() - timedelta(days=days)
    qs = DowntimeLog.objects.filter(
        machine_id=machine_id,
        start_time__date__gte=start,
    )

    by_reason = qs.values('reason_category').annotate(
        count=Count('id'),
        total_min=Sum('duration_min'),
    ).order_by('-total_min')

    # تعداد توقفات هفتگی
    weekly = []
    for week in range(days // 7):
        w_start = date.today() - timedelta(days=(week + 1) * 7)
        w_end = date.today() - timedelta(days=week * 7)
        cnt = qs.filter(start_time__date__range=(w_start, w_end)).count()
        weekly.append({
            'week_start': w_start.isoformat(),
            'count': cnt,
        })

    # MTBF (Mean Time Between Failures)
    total_failures = qs.count()
    total_hours = days * 24
    mtbf = round(total_hours / max(total_failures, 1), 1)

    # MTTR (Mean Time To Repair)
    total_repair_min = qs.aggregate(t=Sum('duration_min'))['t'] or 0
    mttr = round(total_repair_min / max(total_failures, 1), 1)

    # هشدار
    risk_level = 'low'
    if mtbf < 48:
        risk_level = 'critical'
    elif mtbf < 120:
        risk_level = 'high'
    elif mtbf < 240:
        risk_level = 'medium'

    return {
        'machine_id': machine_id,
        'period_days': days,
        'total_failures': total_failures,
        'mtbf_hours': mtbf,
        'mttr_minutes': mttr,
        'risk_level': risk_level,
        'by_reason': list(by_reason),
        'weekly_trend': list(reversed(weekly)),
    }

"""
Diaco MES - Dashboard Views
==============================
داشبورد اصلی با KPIهای تولید + مانیتورینگ زنده خطوط.
شامل KPIهای v2.0: بوبین‌پیچی، دولاتابی TFO، هیت‌ست.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F, DecimalField, Avg
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import json
import jdatetime

from apps.orders.models import Order
from apps.inventory.models import FiberStock, DyeStock, ChemicalStock
from apps.core.models import ProductionLine, Machine, Shift
from apps.maintenance.models import WorkOrder, Schedule
from apps.blowroom.models import Batch as BlowroomBatch
from apps.carding.models import Production as CardingProduction
from apps.passage.models import Production as PassageProduction
from apps.finisher.models import Production as FinisherProduction
from apps.spinning.models import Production as SpinningProduction
from apps.dyeing.models import Batch as DyeingBatch
from apps.winding.models import Production as WindingProduction
from apps.tfo.models import Production as TFOProduction
from apps.heatset.models import Batch as HeatsetBatch


@login_required
def index(request):
    """داشبورد اصلی MES."""
    today = date.today()
    lines = ProductionLine.objects.filter(status='active')

    # ── سفارشات ─────────────────────────────────────────
    orders_qs = Order.objects.all()
    orders_stats = {
        'total': orders_qs.count(),
        'active': orders_qs.filter(status__in=['confirmed', 'in_production', 'quality_check']).count(),
        'draft': orders_qs.filter(status='draft').count(),
        'delivered': orders_qs.filter(status='delivered').count(),
        'overdue': orders_qs.filter(
            delivery_date__lt=today
        ).exclude(status__in=['delivered', 'cancelled']).count(),
    }

    # ── انبار ────────────────────────────────────────────
    fiber_total = FiberStock.objects.filter(status='available').aggregate(
        total_weight=Sum('current_weight')
    )['total_weight'] or 0
    dye_count = DyeStock.objects.filter(status='available').count()
    chemical_count = ChemicalStock.objects.filter(status='available').count()

    inventory_stats = {
        'fiber_weight': fiber_total,
        'dye_count': dye_count,
        'chemical_count': chemical_count,
    }

    # ── نگهداری ──────────────────────────────────────────
    wo_open = WorkOrder.objects.filter(status__in=['open', 'in_progress']).count()
    pm_overdue = Schedule.objects.filter(
        is_active=True,
        next_due_at__lt=timezone.now()
    ).count()

    maintenance_stats = {
        'wo_open': wo_open,
        'pm_overdue': pm_overdue,
    }

    # ── سفارشات اخیر ─────────────────────────────────────
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]

    # ── دستور کارهای باز ─────────────────────────────────
    open_workorders = WorkOrder.objects.select_related('machine').filter(
        status__in=['open', 'in_progress']
    ).order_by('-created_at')[:5]

    # ── KPI تکمیل نخ v2.0 (امروز) ───────────────────────
    wd_today  = WindingProduction.objects.filter(production_date=today)
    tfo_today = TFOProduction.objects.filter(production_date=today)
    hs_today  = HeatsetBatch.objects.filter(production_date=today)

    v2_kpi = {
        # بوبین‌پیچی
        'wd_batches':        wd_today.count(),
        'wd_output_kg':      float(wd_today.aggregate(
            s=Coalesce(Sum('output_weight_kg'), Decimal('0'), output_field=DecimalField()))['s']),
        'wd_avg_cuts':       round(float(
            wd_today.filter(cuts_per_100km__isnull=False)
                    .aggregate(a=Avg('cuts_per_100km'))['a'] or 0), 1),
        'wd_avg_efficiency': round(float(
            wd_today.filter(efficiency_pct__isnull=False)
                    .aggregate(a=Avg('efficiency_pct'))['a'] or 0), 1),
        # دولاتابی TFO
        'tfo_batches':          tfo_today.count(),
        'tfo_output_kg':        float(tfo_today.aggregate(
            s=Coalesce(Sum('output_weight_kg'), Decimal('0'), output_field=DecimalField()))['s']),
        'tfo_avg_efficiency':   round(float(
            tfo_today.filter(efficiency_pct__isnull=False)
                     .aggregate(a=Avg('efficiency_pct'))['a'] or 0), 1),
        'tfo_total_breakage':   tfo_today.aggregate(
            s=Coalesce(Sum('breakage_count'), 0))['s'] or 0,
        # هیت‌ست
        'hs_batches':   hs_today.count(),
        'hs_pass':      hs_today.filter(quality_result='pass').count(),
        'hs_fail':      hs_today.filter(quality_result='fail').count(),
        'hs_total_kg':  float(hs_today.aggregate(
            s=Coalesce(Sum('batch_weight_kg'), Decimal('0'), output_field=DecimalField()))['s']),
    }
    total_hs = v2_kpi['hs_batches']
    v2_kpi['hs_pass_rate'] = (
        round(v2_kpi['hs_pass'] / total_hs * 100, 1) if total_hs > 0 else None
    )

    context = {
        'lines': lines,
        'orders_stats': orders_stats,
        'inventory_stats': inventory_stats,
        'maintenance_stats': maintenance_stats,
        'recent_orders': recent_orders,
        'open_workorders': open_workorders,
        'v2_kpi': v2_kpi,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def line_monitor(request):
    """صفحه مانیتورینگ زنده خطوط تولید."""
    lines = ProductionLine.objects.all().order_by('code')
    return render(request, 'dashboard/line_monitor.html', {'lines': lines})


@login_required
def line_monitor_api(request):
    """API لحظه‌ای خطوط تولید — رفرش هر ۳۰ ثانیه."""
    today = date.today()
    lines = ProductionLine.objects.all().order_by('code')
    data = []

    for line in lines:
        line_data = {
            'id': line.id,
            'code': line.code,
            'name': line.name,
            'status': line.status,
            'status_display': line.get_status_display(),
            'product_type': line.product_type or '-',
            'target_capacity_kg': float(line.target_capacity_kg) if line.target_capacity_kg else 0,
            'machines': _get_line_machines(line),
            'stages': _get_line_stages(line, today),
            'today_production': _get_today_production(line, today),
        }
        if line.target_capacity_kg and line.target_capacity_kg > 0:
            total_produced = line_data['today_production']['total_output_kg']
            line_data['capacity_pct'] = min(
                round(float(total_produced) / float(line.target_capacity_kg) * 100, 1), 100
            )
        else:
            line_data['capacity_pct'] = 0
        data.append(line_data)

    return JsonResponse({'lines': data, 'timestamp': timezone.now().isoformat()})


def _get_line_machines(line):
    machines = Machine.objects.filter(production_line=line)
    return {
        'total': machines.count(),
        'active': machines.filter(status='active').count(),
        'maintenance': machines.filter(status='maintenance').count(),
        'inactive': machines.filter(status='inactive').count(),
    }


def _get_line_stages(line, today):
    """۹ مرحله کامل زنجیره تولید نخ فرش"""
    stages = []
    for name, key, icon, color, Model, fk, active_statuses, extra in [
        # name, key, icon, color, Model, filter_kwargs, active_status_list, extra_fields
        # حلاجی — باز کردن و مخلوط الیاف خام با هوا (tornado = گردباد هوا)
        ('حلاجی',      'blowroom',  'ti ti-tornado',                '#6366f1', BlowroomBatch,      {'production_line': line}, ['in_progress'], {}),
        # کاردینگ — شانه‌زنی الیاف با سوزن‌های ریز روی سیلندر
        ('کاردینگ',    'carding',   'ti ti-needle',                 '#8b5cf6', CardingProduction,  {'production_line': line}, ['in_progress'], {}),
        # پاساژ — ادغام و کشش چند فتیله روی هم (layers)
        ('پاساژ',      'passage',   'ti ti-layers-intersect',       '#a855f7', PassageProduction,  {'production_line': line}, ['in_progress'], {}),
        # فینیشر — آخرین تنظیم ضخامت فتیله قبل از رینگ
        ('فینیشر',     'finisher',  'ti ti-adjustments-horizontal', '#ec4899', FinisherProduction, {'production_line': line}, ['in_progress'], {}),
        # رینگ — چرخش اسپیندل و تابیدن نخ (fidget-spinner = اسپیندل چرخان)
        ('رینگ',       'spinning',  'ti ti-fidget-spinner',         '#ef4444', SpinningProduction, {'production_line': line}, ['in_progress'], {}),
        # بوبین‌پیچی — پیچیدن نخ دور بوبین استوانه‌ای
        ('بوبین‌پیچی', 'winding',   'ti ti-cylinder',               '#f97316', WindingProduction,  {'production_line': line}, ['in_progress'], {'speed': 'winding_speed_mpm', 'efficiency': 'efficiency_pct'}),
        # دولاتابی TFO — تاب دوگانه (infinity = حرکت ∞ شکل)
        ('دولاتابی',   'tfo',       'ti ti-infinity',               '#eab308', TFOProduction,      {'production_line': line}, ['in_progress'], {'tpm': 'twist_tpm', 'efficiency': 'efficiency_pct'}),
        # هیت‌ست — تثبیت تاب با بخار/حرارت در اتوکلاو
        ('هیت‌ست',     'heatset',   'ti ti-flame',                  '#f43f5e', HeatsetBatch,       {'production_line': line}, ['processing','loading','cooling'], {'temp': 'temperature_c'}),
        # رنگرزی — غوطه‌ور در محلول رنگ (droplet-filled)
        ('رنگرزی',     'dyeing',    'ti ti-droplet-filled',         '#06b6d4', DyeingBatch,        {'machine__production_line': line}, ['in_progress'], {}),
    ]:
        last = Model.objects.filter(**fk).order_by('-production_date', '-created_at').first()
        stages.append(_stage_info(name, key, icon, color, last, today, active_statuses, extra))
    return stages


def _stage_info(name, key, icon, color, last_batch, today, active_statuses, extra_fields):
    if last_batch:
        prod_date = last_batch.production_date
        is_active = prod_date == today and last_batch.status in active_statuses
        machine = getattr(last_batch, 'machine', None)
        machine_code = machine.code if machine else '-'

        # اطلاعات اضافه بر اساس نوع مرحله
        extra_data = {}
        for label, field in extra_fields.items():
            val = getattr(last_batch, field, None)
            extra_data[label] = float(val) if val is not None else None

        # اطلاعات کیفی هیت‌ست
        quality = None
        if hasattr(last_batch, 'quality_result'):
            quality = last_batch.quality_result

        return {
            'name': name, 'key': key, 'icon': icon, 'color': color,
            'has_data': True, 'active_now': is_active,
            'last_batch': last_batch.batch_number,
            'last_status': last_batch.status,
            'last_status_display': last_batch.get_status_display(),
            'last_date': jdatetime.date.fromgregorian(date=prod_date).strftime('%Y/%m/%d'),
            'machine_code': machine_code,
            'quality': quality,
            'extra': extra_data,
        }
    return {
        'name': name, 'key': key, 'icon': icon, 'color': color,
        'has_data': False, 'active_now': False,
        'last_batch': '-', 'last_status': 'idle',
        'last_status_display': 'بدون تولید',
        'last_date': '-', 'machine_code': '-',
        'quality': None, 'extra': {},
    }


def _get_today_production(line, today):
    def agg(Model, fk, field):
        return float(Model.objects.filter(production_date=today, **fk).aggregate(
            s=Coalesce(Sum(field), Decimal('0'), output_field=DecimalField()))['s'])

    bl_kg  = agg(BlowroomBatch,     {'production_line': line},           'output_weight')
    sp_kg  = agg(SpinningProduction, {'production_line': line},           'output_weight')
    wd_kg  = agg(WindingProduction,  {'production_line': line},           'output_weight_kg')
    tfo_kg = agg(TFOProduction,      {'production_line': line},           'output_weight_kg')
    hs_kg  = agg(HeatsetBatch,       {'production_line': line},           'batch_weight_kg')
    dy_kg  = agg(DyeingBatch,        {'machine__production_line': line},  'fiber_weight')

    active = 0
    for Model, fk, statuses in [
        (BlowroomBatch,     {'production_line': line},          ['in_progress']),
        (CardingProduction, {'production_line': line},          ['in_progress']),
        (PassageProduction, {'production_line': line},          ['in_progress']),
        (FinisherProduction,{'production_line': line},          ['in_progress']),
        (SpinningProduction,{'production_line': line},          ['in_progress']),
        (WindingProduction, {'production_line': line},          ['in_progress']),
        (TFOProduction,     {'production_line': line},          ['in_progress']),
        (HeatsetBatch,      {'production_line': line},          ['loading','processing','cooling']),
        (DyeingBatch,       {'machine__production_line': line}, ['in_progress']),
    ]:
        active += Model.objects.filter(production_date=today, status__in=statuses, **fk).count()

    return {
        'blowroom_kg':  bl_kg,
        'spinning_kg':  sp_kg,
        'winding_kg':   wd_kg,
        'tfo_kg':       tfo_kg,
        'heatset_kg':   hs_kg,
        'dyeing_kg':    dy_kg,
        'active_batches': active,
        'total_output_kg': sp_kg + wd_kg + tfo_kg + hs_kg,
        'blowroom_count': BlowroomBatch.objects.filter(production_date=today, production_line=line).count(),
        'spinning_count': SpinningProduction.objects.filter(production_date=today, production_line=line).count(),
        'winding_count':  WindingProduction.objects.filter(production_date=today, production_line=line).count(),
        'tfo_count':      TFOProduction.objects.filter(production_date=today, production_line=line).count(),
        'heatset_count':  HeatsetBatch.objects.filter(production_date=today, production_line=line).count(),
        'dyeing_count':   DyeingBatch.objects.filter(production_date=today, machine__production_line=line).count(),
    }


# ═══════════════════════════════════════════════════════════════
# FLOOR MAP
# ═══════════════════════════════════════════════════════════════

@login_required
def floor_map(request):
    return render(request, 'dashboard/floor_map.html', {'page_title': 'نقشه کارگاه'})


@login_required
def floor_map_api(request):
    today = date.today()
    now = timezone.now()
    h = now.hour
    if 6 <= h < 14:
        shift_name = 'شیفت صبح'
    elif 14 <= h < 22:
        shift_name = 'شیفت عصر'
    else:
        shift_name = 'شیفت شب'

    machines = Machine.objects.select_related('production_line').all()
    type_model_map = {
        'blowroom': BlowroomBatch,
        'carding': CardingProduction,
        'passage': PassageProduction,
        'finisher': FinisherProduction,
        'ring': SpinningProduction,
        'winding': WindingProduction,
        'tfo': TFOProduction,
    }
    result = []

    for m in machines:
        data = {
            'id': m.id, 'code': m.code, 'name': m.name,
            'type': m.machine_type, 'status': m.status,
            'status_display': m.get_status_display(),
            'line_code': m.production_line.code if m.production_line else '-',
            'shift': shift_name, 'efficiency': 0, 'output_kg': 0,
            'last_batch': '-', 'batch_status': 'idle', 'heat_level': 'idle',
        }

        if m.status == 'maintenance':
            data['heat_level'] = 'maintenance'
            result.append(data)
            continue
        if m.status != 'active':
            result.append(data)
            continue

        Model = type_model_map.get(m.machine_type)
        if Model:
            today_qs = Model.objects.filter(machine=m, production_date=today).order_by('-created_at')
            last = today_qs.first()
            if last:
                data['last_batch'] = last.batch_number
                data['batch_status'] = last.status
                for f in ('output_weight_kg', 'output_weight', 'fiber_weight'):
                    if hasattr(last, f):
                        total = today_qs.aggregate(s=Sum(f))['s']
                        data['output_kg'] = float(total or 0)
                        break
                if hasattr(last, 'efficiency_pct') and last.efficiency_pct:
                    avg = today_qs.filter(efficiency_pct__isnull=False).aggregate(a=Avg('efficiency_pct'))['a']
                    data['efficiency'] = round(float(avg or 0), 1)

        eff = data['efficiency']
        if data['batch_status'] in ('in_progress', 'processing'):
            data['heat_level'] = 'good' if eff >= 90 else ('warning' if eff >= 70 else 'critical')
        elif data['batch_status'] == 'completed' and eff > 0:
            data['heat_level'] = 'good'

        result.append(data)

    jd = jdatetime.date.fromgregorian(date=today)
    return JsonResponse({
        'machines': result,
        'timestamp': now.isoformat(),
        'jalali_date': jd.strftime('%Y/%m/%d'),
        'shift': shift_name,
        'summary': {
            'total': len(result),
            'active': sum(1 for r in result if r['heat_level'] == 'good'),
            'warning': sum(1 for r in result if r['heat_level'] == 'warning'),
            'critical': sum(1 for r in result if r['heat_level'] == 'critical'),
            'maintenance': sum(1 for r in result if r['heat_level'] == 'maintenance'),
            'idle': sum(1 for r in result if r['heat_level'] == 'idle'),
        }
    })

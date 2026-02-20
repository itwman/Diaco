"""
Diaco MES - Tablet Operator Views (بازطراحی شده)
====================================
رابط تبلت: ثبت سریع تولید توسط سرشیفت.

اصول طراحی:
 - سرشیفت فقط اطلاعات لحظه‌ای شیفت را وارد می‌کند
 - پارامترهای ثابت ماشین از specs ماشین خوانده می‌شود
 - راندمان خودکار از دوک‌های فعال/کل محاسبه می‌شود
 - ضایعات خودکار از ورودی - خروجی محاسبه می‌شود
 - JSON دیگر از کاربر گرفته نمی‌شود
"""
import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from apps.core.models import ProductionLine, Machine, Shift
from apps.orders.models import Order
from apps.blowroom.models import Batch as BlowroomBatch, BatchInput
from apps.carding.models import Production as CardingProd
from apps.passage.models import Production as PassageProd
from apps.finisher.models import Production as FinisherProd
from apps.spinning.models import Production as SpinningProd
from apps.winding.models import Production as WindingProd
from apps.tfo.models import Production as TFOProd
from apps.heatset.models import Batch as HeatsetBatch, CycleLog
from apps.inventory.models import FiberStock
from apps.maintenance.models import DowntimeLog, WorkOrder
from apps.core.batch_utils import next_batch_number


# ══════════════════════════════════════════════════════════════
# ابزارهای مشترک
# ══════════════════════════════════════════════════════════════

def _next_batch(prefix, model):
    """شماره بچ بعدی — تاریخ شمسی | مثال: BL-040929-001"""
    return next_batch_number(prefix, model)


def _get_shift(line=None):
    """تشخیص شیفت جاری بر اساس ساعت."""
    h = datetime.now().hour
    name_map = {(6, 14): 'صبح', (14, 22): 'عصر'}
    shift_name = 'شب'
    for (start, end), name in name_map.items():
        if start <= h < end:
            shift_name = name
            break
    if line:
        shift = Shift.objects.filter(
            production_line=line, name__icontains=shift_name
        ).first()
        if shift:
            return shift
    shift = Shift.objects.filter(
        production_line__isnull=True, name__icontains=shift_name
    ).first()
    if shift:
        return shift
    return Shift.objects.filter(name__icontains=shift_name).first() or Shift.objects.first()


_SECTION_MAP = {
    'حلاجی': 'blowroom',
    'کاردینگ': 'carding',
    'پاساژ': 'passage',
    'فینیشر': 'finisher',
    'رینگ': 'ring',
}


def _machines(section, line=None):
    """ماشین‌آلات فعال بخش مشخص."""
    mt = _SECTION_MAP.get(section, section)
    qs = Machine.objects.filter(status='active', machine_type=mt)
    if line:
        qs = qs.filter(production_line=line)
    return qs


def _get_selected_line(request):
    """خط تولید انتخاب‌شده از session."""
    line_id = request.GET.get('line') or request.session.get('tablet_line')
    if line_id:
        try:
            line = ProductionLine.objects.get(pk=line_id, status='active')
            request.session['tablet_line'] = line.id
            return line
        except ProductionLine.DoesNotExist:
            pass
    return None


def _get_active_lines():
    return ProductionLine.objects.filter(status='active').order_by('code')


def _base_context(request):
    line = _get_selected_line(request)
    return {
        'lines': _get_active_lines(),
        'selected_line': line,
    }


def _safe_decimal(val, default=None):
    """تبدیل ایمن به Decimal."""
    if val is None or str(val).strip() == '':
        return default
    try:
        return Decimal(str(val))
    except (InvalidOperation, ValueError):
        return default


def _safe_int(val, default=None):
    """تبدیل ایمن به int."""
    if val is None or str(val).strip() == '':
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# ══════════════════════════════════════════════════════════════
# انتخاب خط تولید
# ══════════════════════════════════════════════════════════════

@login_required
def select_line(request):
    if request.method == 'POST':
        line_id = request.POST.get('line')
        if line_id:
            request.session['tablet_line'] = int(line_id)
        return redirect('tablet:home')
    return render(request, 'tablet/select_line.html', {
        'lines': _get_active_lines(),
    })


# ══════════════════════════════════════════════════════════════
# صفحه خانه
# ══════════════════════════════════════════════════════════════

@login_required
def home(request):
    ctx = _base_context(request)
    today = date.today()
    line = ctx['selected_line']
    records = []

    for label, Model in [
        ('حلاجی', BlowroomBatch), ('کاردینگ', CardingProd),
        ('پاساژ', PassageProd), ('فینیشر', FinisherProd), ('رینگ', SpinningProd),
        ('بوبین‌پیچی', WindingProd), ('دولاتابی', TFOProd),
    ]:
        qs = Model.objects.filter(
            operator=request.user, production_date=today
        ).select_related('machine')
        if line:
            qs = qs.filter(production_line=line)
        for item in qs:
            records.append({
                'section': label,
                'batch_number': item.batch_number,
                'machine': item.machine.code,
                'status': item.status,
            })

    # هیت‌ست امروز (مدل جداگانه با batch_number)
    hs_qs = HeatsetBatch.objects.filter(
        operator=request.user, production_date=today
    ).select_related('machine')
    if line:
        hs_qs = hs_qs.filter(production_line=line)
    for item in hs_qs:
        records.append({
            'section': 'هیت‌ست',
            'batch_number': item.batch_number,
            'machine': item.machine.code,
            'status': item.status,
        })

    # توقفات امروز
    today_downtimes = DowntimeLog.objects.filter(
        operator=request.user,
        start_time__date=today,
    ).select_related('machine').order_by('-start_time')[:5]

    ctx['today_records'] = records
    ctx['today_downtimes'] = today_downtimes
    return render(request, 'tablet/home.html', ctx)


# ══════════════════════════════════════════════════════════════
# حلاجی — با انتخاب بصری الیاف (بدون JSON)
# ══════════════════════════════════════════════════════════════

@login_required
def blowroom_form(request):
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            # ضایعات خودکار
            inp_w = _safe_decimal(request.POST.get('total_input_weight'))
            out_w = _safe_decimal(request.POST.get('output_weight'))
            waste_w = _safe_decimal(request.POST.get('waste_weight'))
            if inp_w and out_w and not waste_w:
                waste_w = max(Decimal('0'), inp_w - out_w)

            batch = BlowroomBatch(
                production_line=line,
                batch_number=_next_batch('BL', BlowroomBatch),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                total_input_weight=inp_w,
                output_weight=out_w,
                waste_weight=waste_w,
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            if request.POST.get('order'):
                batch.order_id = request.POST['order']

            # ساخت blend_recipe از ردیف‌های الیاف (بدون JSON دستی)
            fiber_ids = request.POST.getlist('fiber_stock[]')
            fiber_weights = request.POST.getlist('fiber_weight[]')
            recipe = {}
            total_fiber = Decimal('0')
            fiber_rows = []  # برای ذخیره در BatchInput

            for fid, fw in zip(fiber_ids, fiber_weights):
                fid = fid.strip()
                fw_dec = _safe_decimal(fw)
                if fid and fw_dec and fw_dec > 0:
                    try:
                        fs = FiberStock.objects.get(pk=fid, status='available')
                        recipe[fs.category.code] = float(fw_dec)
                        total_fiber += fw_dec
                        fiber_rows.append((fs, fw_dec))
                    except FiberStock.DoesNotExist:
                        pass

            # تبدیل به درصد در recipe
            if total_fiber > 0:
                batch.blend_recipe = {
                    k: round(v / float(total_fiber) * 100, 1)
                    for k, v in recipe.items()
                }

            batch.save()

            # ذخیره BatchInput‌ها
            for fs, fw_dec in fiber_rows:
                pct = round(float(fw_dec) / float(total_fiber) * 100, 2) if total_fiber else None
                BatchInput.objects.create(
                    batch=batch,
                    fiber_stock=fs,
                    weight_used=fw_dec,
                    percentage=pct,
                )

            messages.success(request, f'بچ حلاجی {batch.batch_number} ثبت شد ✓')
            return redirect('tablet:home')

        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    orders = Order.objects.filter(status__in=['confirmed', 'in_production'])
    if line:
        orders = orders.filter(Q(production_line=line) | Q(production_line__isnull=True))

    # الیاف موجود در انبار برای انتخاب بصری
    fiber_stocks = FiberStock.objects.filter(
        status='available',
        current_weight__gt=0,
    ).select_related('category').order_by('category__name', '-received_date')

    ctx['machines'] = _machines('حلاجی', line)
    ctx['orders'] = orders.order_by('-created_at')[:20]
    ctx['fiber_stocks'] = fiber_stocks
    return render(request, 'tablet/blowroom_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# کاردینگ
# ══════════════════════════════════════════════════════════════

@login_required
def carding_form(request):
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            inp_w = _safe_decimal(request.POST.get('input_weight'))
            out_w = _safe_decimal(request.POST.get('output_weight'))
            waste_w = _safe_decimal(request.POST.get('waste_weight'))
            if inp_w and out_w and not waste_w:
                waste_w = max(Decimal('0'), inp_w - out_w)

            prod = CardingProd(
                production_line=line,
                batch_number=_next_batch('CR', CardingProd),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                blowroom_batch_id=request.POST['blowroom_batch'],
                speed_rpm=_safe_decimal(request.POST.get('speed_rpm')),
                sliver_count=_safe_decimal(request.POST.get('sliver_count')) or Decimal('1'),
                sliver_weight_gperm=_safe_decimal(request.POST.get('sliver_weight_gperm')),
                input_weight=inp_w,
                output_weight=out_w,
                waste_weight=waste_w,
                neps_count=_safe_int(request.POST.get('neps_count')),
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ کاردینگ {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    blowroom_qs = BlowroomBatch.objects.filter(status='completed').order_by('-production_date')
    if line:
        blowroom_qs = blowroom_qs.filter(production_line=line)
    ctx['machines'] = _machines('کاردینگ', line)
    ctx['blowroom_batches'] = blowroom_qs[:30]
    return render(request, 'tablet/carding_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# پاساژ
# ══════════════════════════════════════════════════════════════

@login_required
def passage_form(request):
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            inp_w = _safe_decimal(request.POST.get('input_total_weight'))
            out_w = _safe_decimal(request.POST.get('output_weight'))

            prod = PassageProd(
                production_line=line,
                batch_number=_next_batch('PS', PassageProd),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                passage_number=_safe_int(request.POST.get('passage_number'), 1),
                num_inputs=_safe_int(request.POST.get('num_inputs'), 6),
                draft_ratio=_safe_decimal(request.POST.get('draft_ratio')),
                output_sliver_count=_safe_decimal(request.POST.get('output_sliver_count')) or Decimal('1'),
                output_weight_gperm=_safe_decimal(request.POST.get('output_weight_gperm')),
                input_total_weight=inp_w,
                output_weight=out_w,
                speed_mpm=_safe_decimal(request.POST.get('speed_mpm')),
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ پاساژ {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    carding_qs = CardingProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        carding_qs = carding_qs.filter(production_line=line)

    ctx['machines'] = _machines('پاساژ', line)
    ctx['carding_batches'] = carding_qs[:30]
    return render(request, 'tablet/passage_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# فینیشر
# ══════════════════════════════════════════════════════════════

@login_required
def finisher_form(request):
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            inp_w = _safe_decimal(request.POST.get('input_weight'))
            out_w = _safe_decimal(request.POST.get('output_weight'))

            prod = FinisherProd(
                production_line=line,
                batch_number=_next_batch('FN', FinisherProd),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                passage_production_id=request.POST['passage_production'],
                input_weight=inp_w,
                output_weight=out_w,
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ فینیشر {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    passage_qs = PassageProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        passage_qs = passage_qs.filter(production_line=line)
    ctx['machines'] = _machines('فینیشر', line)
    ctx['passage_batches'] = passage_qs[:30]
    return render(request, 'tablet/finisher_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# رینگ — راندمان خودکار، بدون پارامترهای فنی
# ══════════════════════════════════════════════════════════════

@login_required
def spinning_form(request):
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            active = _safe_int(request.POST.get('num_spindles_active'))
            total = _safe_int(request.POST.get('num_spindles_total'))
            # راندمان خودکار
            eff = _safe_decimal(request.POST.get('efficiency_pct'))
            if not eff and active and total and total > 0:
                eff = Decimal(str(round(active / total * 100, 2)))

            inp_w = _safe_decimal(request.POST.get('input_weight'))
            out_w = _safe_decimal(request.POST.get('output_weight'))

            # اطلاعات پایه‌ای از specs ماشین (در صورت وجود)
            machine_id = request.POST.get('machine')
            yarn_count = Decimal('30')  # مقدار پیش‌فرض
            twist_tpm = Decimal('850')
            ring_diameter = None
            if machine_id:
                try:
                    m = Machine.objects.get(pk=machine_id)
                    specs = m.specs or {}
                    if specs.get('yarn_count'):
                        yarn_count = Decimal(str(specs['yarn_count']))
                    if specs.get('twist_tpm'):
                        twist_tpm = Decimal(str(specs['twist_tpm']))
                    if specs.get('ring_diameter'):
                        ring_diameter = Decimal(str(specs['ring_diameter']))
                    if specs.get('num_spindles'):
                        total = total or int(specs['num_spindles'])
                except Machine.DoesNotExist:
                    pass

            prod = SpinningProd(
                production_line=line,
                batch_number=_next_batch('SP', SpinningProd),
                machine_id=machine_id,
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                finisher_production_id=request.POST.get('finisher_production') or None,
                yarn_count=yarn_count,
                twist_tpm=twist_tpm,
                twist_direction=request.POST.get('twist_direction', 'Z'),
                spindle_speed_rpm=12000,  # پیش‌فرض — از specs ماشین می‌آید
                ring_diameter=ring_diameter,
                num_spindles_active=active,
                num_spindles_total=total,
                input_weight=inp_w,
                output_weight=out_w,
                breakage_count=_safe_int(request.POST.get('breakage_count'), 0),
                efficiency_pct=eff,
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ رینگ {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    finisher_qs = FinisherProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        finisher_qs = finisher_qs.filter(production_line=line)
    ctx['machines'] = _machines('رینگ', line)
    ctx['finisher_batches'] = finisher_qs[:30]
    return render(request, 'tablet/spinning_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# ثبت توقف — جدید
# ══════════════════════════════════════════════════════════════

@login_required
def downtime_form(request):
    """ثبت توقف ماشین توسط سرشیفت."""
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            machine_id = request.POST.get('machine')
            reason_cat = request.POST.get('reason_category')
            reason_detail = request.POST.get('reason_detail', '').strip()
            duration_min = _safe_int(request.POST.get('duration_min'))
            prod_loss = _safe_decimal(request.POST.get('production_loss'))

            if not reason_detail:
                reason_detail = dict(DowntimeLog.ReasonCategory.choices).get(reason_cat, reason_cat)

            # زمان شروع: از ورودی یا همین لحظه — بدون timezone (USE_TZ=False)
            start_str = request.POST.get('start_time', '')
            if start_str:
                try:
                    start_dt = datetime.strptime(
                        date.today().strftime('%Y-%m-%d') + ' ' + start_str, '%Y-%m-%d %H:%M'
                    )
                except ValueError:
                    start_dt = datetime.now()
            else:
                start_dt = datetime.now()

            # زمان پایان
            end_dt = None
            if duration_min:
                from datetime import timedelta
                end_dt = start_dt + timedelta(minutes=duration_min)

            shift = _get_shift(line)
            if shift is None:
                messages.error(request, 'شیفت فعال یافت نشد — ابتدا شیفت تعریف کنید')
                return redirect('tablet:downtime_form')

            log = DowntimeLog(
                production_line=line,
                machine_id=machine_id,
                operator=request.user,
                shift=shift,
                start_time=start_dt,
                end_time=end_dt,
                duration_min=duration_min,
                reason_category=reason_cat,
                reason_detail=reason_detail,
                production_loss=prod_loss,
                notes=request.POST.get('notes', ''),
            )
            log.save()

            # اگر توقف اضطراری → دستور کار خودکار
            if reason_cat in ('mechanical', 'electrical'):
                from apps.core.batch_utils import next_workorder_number
                wo_num = next_workorder_number(log.pk)
                WorkOrder.objects.create(
                    wo_number=wo_num,
                    machine_id=machine_id,
                    title=f"توقف {log.get_reason_category_display()} — {reason_detail[:50]}",
                    wo_type='corrective',
                    priority='high',
                    reported_by=request.user,
                    status='open',
                )
                messages.success(
                    request,
                    f'توقف ثبت شد و دستور کار {wo_num} صادر شد ✓'
                )
            else:
                messages.success(request, 'توقف با موفقیت ثبت شد ✓')

            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت توقف: {e}')

    # همه ماشین‌های فعال
    all_machines = Machine.objects.filter(status='active').order_by('machine_type', 'code')
    if line:
        all_machines = all_machines.filter(production_line=line)

    ctx['all_machines'] = all_machines
    ctx['reason_choices'] = DowntimeLog.ReasonCategory.choices
    return render(request, 'tablet/downtime_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# بوبین‌پیچی (Winding) — v2.0
# ══════════════════════════════════════════════════════════════

@login_required
def winding_form(request):
    """ثبت تولید بوبین‌پیچی — رابط تبلت اپراتور"""
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            inp_w  = _safe_decimal(request.POST.get('input_weight'))
            out_w  = _safe_decimal(request.POST.get('output_weight'))
            waste_w = _safe_decimal(request.POST.get('waste_weight'))
            if inp_w and out_w and not waste_w:
                waste_w = max(Decimal('0'), inp_w - out_w)

            prod = WindingProd(
                production_line=line,
                batch_number=_next_batch('WD', WindingProd),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                order_id=request.POST.get('order') or None,
                spinning_production_id=request.POST.get('spinning_production') or None,
                input_cops=_safe_int(request.POST.get('input_cops')),
                input_weight_kg=inp_w,
                output_packages=_safe_int(request.POST.get('output_packages')),
                output_weight_kg=out_w,
                waste_weight_kg=waste_w,
                package_type=request.POST.get('package_type', 'cone'),
                winding_speed_mpm=_safe_decimal(request.POST.get('winding_speed_mpm')),
                cuts_per_100km=_safe_int(request.POST.get('cuts_per_100km')),
                efficiency_pct=_safe_decimal(request.POST.get('efficiency_pct')),
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ بوبین‌پیچی {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    spinning_qs = SpinningProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        spinning_qs = spinning_qs.filter(production_line=line)

    ctx['machines'] = Machine.objects.filter(machine_type='winding', status='active')
    ctx['spinning_batches'] = spinning_qs[:30]
    ctx['orders'] = Order.objects.filter(
        status__in=['confirmed', 'in_production']
    ).order_by('-created_at')[:20]
    return render(request, 'tablet/winding_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# دولاتابی TFO — v2.0
# ══════════════════════════════════════════════════════════════

@login_required
def tfo_form(request):
    """ثبت تولید دولاتابی TFO — رابط تبلت اپراتور"""
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        try:
            inp_w  = _safe_decimal(request.POST.get('input_weight'))
            out_w  = _safe_decimal(request.POST.get('output_weight'))
            waste_w = _safe_decimal(request.POST.get('waste_weight'))
            if inp_w and out_w and not waste_w:
                waste_w = max(Decimal('0'), inp_w - out_w)

            prod = TFOProd(
                production_line=line,
                batch_number=_next_batch('TFO', TFOProd),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                order_id=request.POST.get('order') or None,
                winding_production_id=request.POST.get('winding_production') or None,
                ply_count=_safe_int(request.POST.get('ply_count')) or 2,
                twist_tpm=_safe_decimal(request.POST.get('twist_tpm')) or Decimal('0'),
                twist_direction=request.POST.get('twist_direction', 'S'),
                spindle_speed_rpm=_safe_int(request.POST.get('spindle_speed_rpm')),
                input_packages=_safe_int(request.POST.get('input_packages')),
                input_weight_kg=inp_w,
                output_packages=_safe_int(request.POST.get('output_packages')),
                output_weight_kg=out_w,
                waste_weight_kg=waste_w,
                breakage_count=_safe_int(request.POST.get('breakage_count')) or 0,
                efficiency_pct=_safe_decimal(request.POST.get('efficiency_pct')),
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            prod.save()
            messages.success(request, f'بچ دولاتابی {prod.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    winding_qs = WindingProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        winding_qs = winding_qs.filter(production_line=line)

    ctx['machines'] = Machine.objects.filter(machine_type='tfo', status='active')
    ctx['winding_batches'] = winding_qs[:30]
    ctx['orders'] = Order.objects.filter(
        status__in=['confirmed', 'in_production']
    ).order_by('-created_at')[:20]
    return render(request, 'tablet/tfo_form.html', ctx)


# ══════════════════════════════════════════════════════════════
# هیت‌ست — v2.0
# ══════════════════════════════════════════════════════════════

@login_required
def heatset_form(request):
    """ثبت بچ هیت‌ست + ثبت لاگ چرخه — رابط تبلت اپراتور"""
    ctx = _base_context(request)
    line = ctx['selected_line']

    if request.method == 'POST':
        action = request.POST.get('action', 'create')

        # ── ثبت لاگ چرخه (HTMX) ──────────────────────────────
        if action == 'log':
            batch_id = request.POST.get('batch_id')
            try:
                batch = HeatsetBatch.objects.get(pk=batch_id, operator=request.user)
                log = CycleLog.objects.create(
                    heatset_batch=batch,
                    elapsed_min=_safe_decimal(request.POST.get('elapsed_min')),
                    temperature_c=_safe_decimal(request.POST.get('temperature_c')),
                    pressure_bar=_safe_decimal(request.POST.get('pressure_bar')),
                    phase=request.POST.get('phase', 'steam'),
                )
                from django.http import JsonResponse
                return JsonResponse({'ok': True, 'id': log.id,
                                     'temp': str(log.temperature_c or ''),
                                     'elapsed': str(log.elapsed_min or '')})
            except Exception as e:
                from django.http import JsonResponse
                return JsonResponse({'ok': False, 'error': str(e)}, status=400)

        # ── ایجاد بچ جدید ─────────────────────────────────────
        try:
            batch = HeatsetBatch(
                production_line=line,
                batch_number=_next_batch('HS', HeatsetBatch),
                machine_id=request.POST['machine'],
                operator=request.user,
                shift=_get_shift(line),
                production_date=date.today(),
                order_id=request.POST.get('order') or None,
                tfo_production_id=request.POST.get('tfo_production') or None,
                machine_type_hs=request.POST.get('machine_type_hs', 'autoclave'),
                fiber_type=request.POST.get('fiber_type', 'polyester'),
                cycle_type=request.POST.get('cycle_type', 'standard'),
                temperature_c=_safe_decimal(request.POST.get('temperature_c')) or Decimal('120'),
                steam_pressure_bar=_safe_decimal(request.POST.get('steam_pressure_bar')),
                vacuum_level_mbar=_safe_decimal(request.POST.get('vacuum_level_mbar')),
                pre_heat_min=_safe_int(request.POST.get('pre_heat_min')),
                steam_time_min=_safe_int(request.POST.get('steam_time_min')),
                dwell_time_min=_safe_int(request.POST.get('dwell_time_min')),
                cooldown_min=_safe_int(request.POST.get('cooldown_min')),
                batch_weight_kg=_safe_decimal(request.POST.get('batch_weight_kg')) or Decimal('0'),
                packages_count=_safe_int(request.POST.get('packages_count')),
                quality_result=request.POST.get('quality_result') or None,
                notes=request.POST.get('notes', ''),
                status='completed',
            )
            batch.save()
            messages.success(request, f'بچ هیت‌ست {batch.batch_number} ثبت شد ✓')
            return redirect('tablet:home')
        except Exception as e:
            messages.error(request, f'خطا در ثبت: {e}')

    tfo_qs = TFOProd.objects.filter(status='completed').order_by('-production_date')
    if line:
        tfo_qs = tfo_qs.filter(production_line=line)

    ctx['machines'] = Machine.objects.filter(machine_type='heatset', status='active')
    ctx['tfo_batches'] = tfo_qs[:30]
    ctx['orders'] = Order.objects.filter(
        status__in=['confirmed', 'in_production']
    ).order_by('-created_at')[:20]
    return render(request, 'tablet/heatset_form.html', ctx)

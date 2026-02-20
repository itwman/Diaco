"""
Diaco MES - AI Metadata Signals
==================================
پر کردن خودکار فیلد metadata (JSON) هنگام ذخیره رکوردهای تولید.
این metadata توسط مدل‌های AI/ML برای تحلیل و پیش‌بینی استفاده می‌شود.

ساختار metadata:
{
  "ai_version": "1.0",
  "computed_at": "2026-02-16T12:00:00",
  "oee": { ... },
  "quality_metrics": { ... },
  "anomaly_flags": [ ... ]
}
"""
import json
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.blowroom.models import Batch as BlowroomBatch
from apps.carding.models import Production as CardingProd
from apps.passage.models import Production as PassageProd
from apps.finisher.models import Production as FinisherProd
from apps.spinning.models import Production as SpinningProd
from apps.dyeing.models import Batch as DyeingBatch
from apps.maintenance.models import DowntimeLog


def _base_metadata():
    return {
        'ai_version': '1.0',
        'computed_at': datetime.now().isoformat(),
    }


def _safe_float(val):
    try:
        return float(val) if val is not None else None
    except (ValueError, TypeError):
        return None


# ── حلاجی ────────────────────────────────────────────────

@receiver(post_save, sender=BlowroomBatch)
def enrich_blowroom_metadata(sender, instance, **kwargs):
    meta = _base_metadata()
    inp = _safe_float(instance.total_input_weight)
    out = _safe_float(instance.output_weight)
    waste = _safe_float(instance.waste_weight)

    if inp and inp > 0:
        meta['yield_pct'] = round(((out or 0) / inp) * 100, 2) if out else None
        meta['waste_pct'] = round(((waste or 0) / inp) * 100, 2) if waste else None

    meta['anomaly_flags'] = []
    if meta.get('waste_pct') and meta['waste_pct'] > 8:
        meta['anomaly_flags'].append('HIGH_WASTE')

    if instance.metadata != meta:
        BlowroomBatch.objects.filter(pk=instance.pk).update(metadata=meta)


# ── کاردینگ ──────────────────────────────────────────────

@receiver(post_save, sender=CardingProd)
def enrich_carding_metadata(sender, instance, **kwargs):
    meta = _base_metadata()
    inp = _safe_float(instance.input_weight)
    out = _safe_float(instance.output_weight)

    if inp and inp > 0 and out:
        meta['yield_pct'] = round((out / inp) * 100, 2)

    meta['quality_metrics'] = {}
    neps = instance.neps_count
    if neps is not None:
        meta['quality_metrics']['neps'] = neps
        meta['anomaly_flags'] = []
        if neps > 200:
            meta['anomaly_flags'].append('HIGH_NEPS')
    else:
        meta['anomaly_flags'] = []

    if instance.metadata != meta:
        CardingProd.objects.filter(pk=instance.pk).update(metadata=meta)


# ── پاساژ ───────────────────────────────────────────────

@receiver(post_save, sender=PassageProd)
def enrich_passage_metadata(sender, instance, **kwargs):
    meta = _base_metadata()
    cv = _safe_float(instance.evenness_cv)

    meta['quality_metrics'] = {}
    meta['anomaly_flags'] = []

    if cv is not None:
        meta['quality_metrics']['evenness_cv'] = cv
        if cv > 5.0:
            meta['anomaly_flags'].append('HIGH_CV')

    draft = _safe_float(instance.draft_ratio)
    if draft:
        meta['quality_metrics']['draft_ratio'] = draft

    if instance.metadata != meta:
        PassageProd.objects.filter(pk=instance.pk).update(metadata=meta)


# ── فینیشر ──────────────────────────────────────────────

@receiver(post_save, sender=FinisherProd)
def enrich_finisher_metadata(sender, instance, **kwargs):
    meta = _base_metadata()
    inp = _safe_float(instance.input_weight)
    out = _safe_float(instance.output_weight)

    if inp and inp > 0 and out:
        meta['yield_pct'] = round((out / inp) * 100, 2)

    meta['anomaly_flags'] = []
    if instance.metadata != meta:
        FinisherProd.objects.filter(pk=instance.pk).update(metadata=meta)


# ── رینگ (بحرانی‌ترین برای AI) ──────────────────────────

@receiver(post_save, sender=SpinningProd)
def enrich_spinning_metadata(sender, instance, **kwargs):
    meta = _base_metadata()
    inp = _safe_float(instance.input_weight)
    out = _safe_float(instance.output_weight)
    eff = _safe_float(instance.efficiency_pct)
    brk = instance.breakage_count or 0
    spindles = instance.num_spindles_active or 0

    # بازده وزنی
    if inp and inp > 0 and out:
        meta['yield_pct'] = round((out / inp) * 100, 2)

    # OEE ساده
    meta['oee'] = {}
    if eff:
        meta['oee']['performance'] = eff
    if spindles > 0:
        total = instance.num_spindles_total or spindles
        meta['oee']['availability'] = round((spindles / total) * 100, 2)
    if eff and spindles > 0:
        avail = meta['oee'].get('availability', 100)
        meta['oee']['oee_simple'] = round((avail * eff) / 10000 * 100, 2)

    # کیفیت
    meta['quality_metrics'] = {
        'breakage_count': brk,
        'breakage_per_1000_spindle_hr': round((brk / max(spindles, 1)) * 1000, 1),
    }

    # هشدار آنومالی
    meta['anomaly_flags'] = []
    if eff and eff < 70:
        meta['anomaly_flags'].append('LOW_EFFICIENCY')
    if brk > 50:
        meta['anomaly_flags'].append('HIGH_BREAKAGE')
    if meta['oee'].get('oee_simple') and meta['oee']['oee_simple'] < 60:
        meta['anomaly_flags'].append('LOW_OEE')

    if instance.metadata != meta:
        SpinningProd.objects.filter(pk=instance.pk).update(metadata=meta)


# ── رنگرزی ──────────────────────────────────────────────

@receiver(post_save, sender=DyeingBatch)
def enrich_dyeing_metadata(sender, instance, **kwargs):
    meta = _base_metadata()

    meta['process_params'] = {
        'temperature': _safe_float(instance.temperature),
        'ph': _safe_float(instance.ph_value),
        'liquor_ratio': _safe_float(instance.liquor_ratio),
        'duration_min': instance.duration_min,
    }

    meta['anomaly_flags'] = []
    if instance.quality_result == 'fail':
        meta['anomaly_flags'].append('QUALITY_FAIL')
    temp = _safe_float(instance.temperature)
    if temp and temp > 130:
        meta['anomaly_flags'].append('HIGH_TEMPERATURE')
    ph = _safe_float(instance.ph_value)
    if ph and (ph < 3 or ph > 11):
        meta['anomaly_flags'].append('EXTREME_PH')

    if instance.metadata != meta:
        DyeingBatch.objects.filter(pk=instance.pk).update(metadata=meta)


# ── توقفات (Predictive Maintenance) ─────────────────────

@receiver(post_save, sender=DowntimeLog)
def enrich_downtime_metadata(sender, instance, **kwargs):
    meta = _base_metadata()

    # تعداد توقفات اخیر همین ماشین (۳۰ روز)
    from datetime import timedelta
    from django.db.models import Sum, Count
    thirty_days_ago = datetime.now() - timedelta(days=30)

    recent = DowntimeLog.objects.filter(
        machine=instance.machine,
        start_time__gte=thirty_days_ago,
    ).aggregate(
        count=Count('id'),
        total_min=Sum('duration_min'),
    )

    meta['machine_health'] = {
        'downtime_count_30d': recent['count'] or 0,
        'downtime_total_min_30d': recent['total_min'] or 0,
    }

    meta['anomaly_flags'] = []
    if (recent['count'] or 0) > 10:
        meta['anomaly_flags'].append('FREQUENT_DOWNTIME')
    if (recent['total_min'] or 0) > 500:
        meta['anomaly_flags'].append('EXCESSIVE_DOWNTIME')

    if instance.metadata != meta:
        DowntimeLog.objects.filter(pk=instance.pk).update(metadata=meta)

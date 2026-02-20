"""
Diaco MES - HeatSet Signals (هیت‌ست)
======================================
F.1 — شاخص‌های کیفی خودکار:
  ✦ هشدار اگر quality_result = fail
  ✦ هشدار اگر دما خارج از محدوده مجاز نوع الیاف
  ✦ هشدار اگر shrinkage_pct خارج از حد
  ✦ تکمیل metadata با AI time-series skeleton

محدوده‌های دمایی بر اساس نوع الیاف:
  پلی‌استر:  130-180°C
  اکریلیک:   110-135°C
  نایلون PA:  105-125°C
  پشم:        100-120°C
  پلی‌پروپیلن: 125-165°C
  مخلوط:      110-135°C (محافظه‌کارانه)

محدوده shrinkage قابل قبول: 0.5-3.5%
"""
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Batch

logger = logging.getLogger(__name__)

# محدوده دمایی مجاز بر نوع الیاف (min, max)
FIBER_TEMP_RANGES = {
    'polyester':     (130, 180),
    'acrylic':       (110, 135),
    'nylon':         (105, 125),
    'wool':          (100, 120),
    'polypropylene': (125, 165),
    'blend':         (110, 135),
}

SHRINKAGE_MIN = 0.5
SHRINKAGE_MAX = 3.5


@receiver(pre_save, sender=Batch)
def heatset_pre_save(sender, instance, **kwargs):
    """
    قبل از ذخیره:
    ✦ مقداردهی اولیه metadata با ساختار AI-Ready
    ✦ محاسبه duration_min (جمع مراحل) — مدل save() هم این کار را می‌کند
    """
    if not instance.metadata or not isinstance(instance.metadata, dict):
        instance.metadata = {}

    # skeleton AI-Ready
    if 'ai_quality' not in instance.metadata:
        instance.metadata['ai_quality'] = {
            'temp_curve':     [],   # منحنی دما (از CycleLog پر می‌شود)
            'pressure_curve': [],   # منحنی فشار
            'humidity_log':   [],   # لاگ رطوبت
            'alerts':         [],
        }


@receiver(post_save, sender=Batch)
def heatset_post_save(sender, instance, created, **kwargs):
    """
    بعد از ذخیره:
    ✦ بررسی quality_result = fail → هشدار بحرانی
    ✦ بررسی دما در محدوده مجاز
    ✦ بررسی shrinkage_pct
    ✦ تکمیل metadata
    """
    alerts = []

    # ── هشدار رد کیفی ──────────────────────────────────────
    if instance.quality_result == 'fail':
        alerts.append({
            'level': 'critical',
            'code':  'QUALITY_FAIL',
            'msg':   f'بچ {instance.batch_number} رد شد — نیاز به بررسی فوری',
        })
        logger.warning(
            'HEATSET QUALITY FAIL | batch=%s | machine=%s | fiber=%s | temp=%s',
            instance.batch_number, instance.machine.code,
            instance.fiber_type, instance.temperature_c
        )

    # ── بررسی دما در محدوده مجاز ──────────────────────────
    fiber = instance.fiber_type
    temp  = float(instance.temperature_c) if instance.temperature_c else None
    if temp and fiber in FIBER_TEMP_RANGES:
        t_min, t_max = FIBER_TEMP_RANGES[fiber]
        if temp < t_min:
            alerts.append({
                'level': 'warning',
                'code':  'LOW_TEMPERATURE',
                'msg':   f'دما {temp}°C پایین‌تر از حداقل {t_min}°C برای {fiber}',
            })
        elif temp > t_max:
            alerts.append({
                'level': 'critical',
                'code':  'HIGH_TEMPERATURE',
                'msg':   f'دما {temp}°C بالاتر از حداکثر {t_max}°C برای {fiber} — خطر آسیب به الیاف!',
            })
            logger.error(
                'HEATSET HIGH TEMP | batch=%s | fiber=%s | temp=%s (max=%s)',
                instance.batch_number, fiber, temp, t_max
            )

    # ── بررسی shrinkage ─────────────────────────────────────
    if instance.shrinkage_pct is not None:
        shrink = float(instance.shrinkage_pct)
        if shrink < SHRINKAGE_MIN:
            alerts.append({
                'level': 'warning',
                'code':  'LOW_SHRINKAGE',
                'msg':   f'آنکاژ {shrink}% پایین‌تر از حد مجاز ({SHRINKAGE_MIN}%) — تثبیت ناکافی؟',
            })
        elif shrink > SHRINKAGE_MAX:
            alerts.append({
                'level': 'warning',
                'code':  'HIGH_SHRINKAGE',
                'msg':   f'آنکاژ {shrink}% بالاتر از حد مجاز ({SHRINKAGE_MAX}%) — آسیب احتمالی',
            })

    # ── ذخیره metadata ──────────────────────────────────────
    meta  = instance.metadata or {}
    ai_q  = meta.get('ai_quality', {'temp_curve': [], 'pressure_curve': [], 'humidity_log': [], 'alerts': []})
    ai_q['alerts'] = alerts
    meta['ai_quality']  = ai_q
    meta['has_alerts']  = bool(alerts)
    meta['quality_result'] = instance.quality_result
    meta['fiber_type']     = instance.fiber_type
    meta['temperature_c']  = str(instance.temperature_c)
    if instance.shrinkage_pct:
        meta['shrinkage_pct'] = str(instance.shrinkage_pct)

    Batch.objects.filter(pk=instance.pk).update(metadata=meta)

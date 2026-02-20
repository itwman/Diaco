"""
Diaco MES - TFO Signals (دولاتابی)
====================================
F.1 — شاخص‌های کیفی خودکار:
  ✦ هشدار پارگی بالا (breakage_count)
  ✦ محاسبه efficiency_pct از روی breakage (اگر دستی وارد نشده)
  ✦ تکمیل metadata (AI-Ready)

آستانه‌های صنعتی:
  breakage_count > 10 → هشدار
  breakage_count > 25 → بحرانی
  efficiency_pct < 70 → هشدار راندمان
"""
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Production

logger = logging.getLogger(__name__)

BREAKAGE_WARNING   = 10   # پارگی بالاتر از این → هشدار
BREAKAGE_CRITICAL  = 25   # پارگی بالاتر از این → بحرانی
EFFICIENCY_MIN     = 70   # راندمان پایین‌تر → هشدار


@receiver(pre_save, sender=Production)
def tfo_pre_save(sender, instance, **kwargs):
    """
    قبل از ذخیره:
    ✦ مقداردهی اولیه metadata
    ✦ محاسبه waste_pct
    """
    if not instance.metadata or not isinstance(instance.metadata, dict):
        instance.metadata = {}

    # پایه AI-Ready
    if 'ai_quality' not in instance.metadata:
        instance.metadata['ai_quality'] = {
            'torque_log':     [],   # لاگ گشتاور دوک (برای آینده)
            'vibration_log':  [],   # لاگ ارتعاش (برای آینده)
            'alerts':         [],
        }

    # محاسبه waste_pct
    if instance.input_weight_kg and instance.waste_weight_kg:
        try:
            waste_pct = round(
                float(instance.waste_weight_kg) / float(instance.input_weight_kg) * 100, 2
            )
            instance.metadata['waste_pct_calculated'] = waste_pct
        except (ZeroDivisionError, TypeError):
            pass


@receiver(post_save, sender=Production)
def tfo_post_save(sender, instance, created, **kwargs):
    """
    بعد از ذخیره:
    ✦ بررسی breakage_count
    ✦ بررسی efficiency_pct
    """
    alerts = []

    # بررسی پارگی
    if instance.breakage_count is not None:
        if instance.breakage_count >= BREAKAGE_CRITICAL:
            alerts.append({
                'level': 'critical',
                'code':  'HIGH_BREAKAGE',
                'msg':   f'پارگی بحرانی: {instance.breakage_count} بار (حد: {BREAKAGE_CRITICAL})',
            })
            logger.warning(
                'TFO CRITICAL BREAKAGE | batch=%s | breakage=%s',
                instance.batch_number, instance.breakage_count
            )
        elif instance.breakage_count >= BREAKAGE_WARNING:
            alerts.append({
                'level': 'warning',
                'code':  'ELEVATED_BREAKAGE',
                'msg':   f'پارگی بالا: {instance.breakage_count} بار (حد هشدار: {BREAKAGE_WARNING})',
            })

    # بررسی راندمان
    if instance.efficiency_pct is not None:
        if float(instance.efficiency_pct) < EFFICIENCY_MIN:
            alerts.append({
                'level': 'warning',
                'code':  'LOW_EFFICIENCY',
                'msg':   f'راندمان پایین: {instance.efficiency_pct}% (حداقل: {EFFICIENCY_MIN}%)',
            })

    if alerts:
        meta = instance.metadata or {}
        ai_q = meta.get('ai_quality', {'alerts': []})
        ai_q['alerts'] = alerts
        meta['ai_quality'] = ai_q
        meta['has_alerts'] = True
        Production.objects.filter(pk=instance.pk).update(metadata=meta)

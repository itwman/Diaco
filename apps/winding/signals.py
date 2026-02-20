"""
Diaco MES - Winding Signals (بوبین‌پیچی)
=========================================
F.1 — شاخص‌های کیفی خودکار:
  ✦ محاسبه waste_pct و درج در metadata
  ✦ هشدار اگر cuts_per_100km > آستانه
  ✦ تکمیل خودکار metadata (AI-Ready)

آستانه‌های صنعتی:
  cuts_per_100km < 20  → کیفیت A (عالی)
  cuts_per_100km ≥ 50  → هشدار کیفی → ثبت در metadata
  efficiency_pct  < 65 → هشدار راندمان
"""
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Production

logger = logging.getLogger(__name__)

# آستانه‌های هشدار
CUTS_WARNING_THRESHOLD   = 50   # برش/۱۰۰km بالاتر از این → هشدار
CUTS_CRITICAL_THRESHOLD  = 80   # برش/۱۰۰km بالاتر از این → بحرانی
EFFICIENCY_MIN           = 65   # راندمان پایین‌تر از این → هشدار


@receiver(pre_save, sender=Production)
def winding_pre_save(sender, instance, **kwargs):
    """
    قبل از ذخیره:
    ✦ مقداردهی اولیه metadata اگر خالی است
    ✦ محاسبه waste_pct و ذخیره در metadata
    """
    # اطمینان از وجود metadata
    if not instance.metadata or not isinstance(instance.metadata, dict):
        instance.metadata = {}

    # پایه AI-Ready
    if 'ai_quality' not in instance.metadata:
        instance.metadata['ai_quality'] = {
            'sensor_tension_log': [],   # لاگ کشش سنسور (برای آینده)
            'speed_log':          [],   # لاگ سرعت (برای آینده)
            'alerts':             [],
        }

    # محاسبه waste_pct و ذخیره
    if instance.input_weight_kg and instance.waste_weight_kg:
        try:
            waste_pct = round(
                float(instance.waste_weight_kg) / float(instance.input_weight_kg) * 100, 2
            )
            instance.metadata['waste_pct_calculated'] = waste_pct
        except (ZeroDivisionError, TypeError):
            pass


@receiver(post_save, sender=Production)
def winding_post_save(sender, instance, created, **kwargs):
    """
    بعد از ذخیره:
    ✦ بررسی آستانه cuts_per_100km و ثبت هشدار در metadata
    ✦ بررسی efficiency_pct
    ✦ ذخیره مجدد فقط اگر metadata تغییر کرده
    """
    alerts = []

    # بررسی کیفیت برش
    if instance.cuts_per_100km is not None:
        if instance.cuts_per_100km >= CUTS_CRITICAL_THRESHOLD:
            alerts.append({
                'level': 'critical',
                'code':  'HIGH_CUTS',
                'msg':   f'برش بحرانی: {instance.cuts_per_100km}/100km (حد بحرانی: {CUTS_CRITICAL_THRESHOLD})',
            })
            logger.warning(
                'WINDING CRITICAL CUTS | batch=%s | cuts=%s',
                instance.batch_number, instance.cuts_per_100km
            )
        elif instance.cuts_per_100km >= CUTS_WARNING_THRESHOLD:
            alerts.append({
                'level': 'warning',
                'code':  'ELEVATED_CUTS',
                'msg':   f'برش بالا: {instance.cuts_per_100km}/100km (حد هشدار: {CUTS_WARNING_THRESHOLD})',
            })
            logger.info(
                'WINDING CUTS WARNING | batch=%s | cuts=%s',
                instance.batch_number, instance.cuts_per_100km
            )

    # بررسی راندمان
    if instance.efficiency_pct is not None:
        if float(instance.efficiency_pct) < EFFICIENCY_MIN:
            alerts.append({
                'level': 'warning',
                'code':  'LOW_EFFICIENCY',
                'msg':   f'راندمان پایین: {instance.efficiency_pct}% (حداقل: {EFFICIENCY_MIN}%)',
            })

    # اگر هشداری وجود دارد → ذخیره در metadata (بدون loop)
    if alerts:
        meta = instance.metadata or {}
        ai_q = meta.get('ai_quality', {'alerts': []})
        ai_q['alerts'] = alerts
        meta['ai_quality'] = ai_q
        meta['has_alerts'] = True
        Production.objects.filter(pk=instance.pk).update(metadata=meta)

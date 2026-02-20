"""
Diaco MES - Carding Models (کاردینگ)
=======================================
مرحله دوم تولید: تبدیل الیاف باز شده به فتیله (sliver).

منطق صنعتی:
───────────
Production (تولید کاردینگ):
  ورودی: الیاف از حلاجی (blowroom_batch).
  خروجی: فتیله (sliver) با نمره مشخص.
  پارامترهای کلیدی:
    - speed_rpm: سرعت ماشین (تأثیر بر کیفیت)
    - sliver_count: نمره فتیله (ضخامت خروجی)
    - neps_count: تعداد گره (شاخص کیفیت - برای AI)
    - cleaning_time: زمان تمیزکاری ماشین
  خروجی این مرحله ورودی پاساژ می‌شود.
"""
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """تولید کاردینگ - تبدیل الیاف به فتیله."""

    # ── ارتباط با حلاجی ─────────────────────────────────
    blowroom_batch = models.ForeignKey(
        'blowroom.Batch',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='بچ حلاجی',
        related_name='carding_productions',
    )

    # ── پارامترهای فنی ──────────────────────────────────
    speed_rpm = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, null=True,
        verbose_name='سرعت (RPM)',
    )
    sliver_count = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name='نمره فتیله',
        help_text='نمره (ضخامت) فتیله خروجی',
    )
    sliver_weight_gperm = models.DecimalField(
        max_digits=8, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن فتیله (g/m)',
    )

    # ── وزن ──────────────────────────────────────────────
    input_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن ورودی (kg)',
    )
    output_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن خروجی (kg)',
    )
    waste_weight = models.DecimalField(
        max_digits=10, decimal_places=3,
        blank=True, null=True,
        verbose_name='ضایعات (kg)',
    )
    waste_pct = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='درصد ضایعات',
    )

    # ── نگهداری و کیفیت ─────────────────────────────────
    cleaning_time = models.TimeField(
        blank=True, null=True,
        verbose_name='زمان تمیزکاری',
    )
    last_cleaning_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name='آخرین تمیزکاری',
    )
    neps_count = models.IntegerField(
        blank=True, null=True,
        verbose_name='تعداد گره (Neps)',
        help_text='شاخص کیفیت - مقدار کمتر بهتر (برای AI)',
    )

    class Meta:
        db_table = 'carding_production'
        verbose_name = 'تولید کاردینگ'
        verbose_name_plural = 'تولیدات کاردینگ'
        indexes = [
            models.Index(fields=['production_date'], name='idx_cd_date'),
            models.Index(fields=['machine'], name='idx_cd_machine'),
        ]

"""
Diaco MES - Passage Models (پاساژ/کشش) ⚠️ بحرانی‌ترین ماژول
===============================================================
مرحله سوم تولید: ادغام و کشش چند فتیله به یک فتیله یکنواخت‌تر.

منطق صنعتی:
───────────
Production (تولید پاساژ):
  ⚠️ این ماژول بحرانی است چون MULTI-INPUT → SINGLE-OUTPUT دارد.
  ورودی: ۶ تا ۸ فتیله از بچ‌های مختلف کاردینگ یا پاساژ قبلی.
  خروجی: ۱ فتیله کشیده‌شده با یکنواختی بهتر.
  
  passage_number:
    ۱ = پاساژ اول (ورودی از کاردینگ)
    ۲ = پاساژ دوم (ورودی از پاساژ اول)
  
  draft_ratio: نسبت کشش (مثلاً 6.5 یعنی ۶.۵ برابر کشیده شده)
  evenness_cv: ضریب تغییرات یکنواختی (CV%) - شاخص کلیدی AI

Input (ورودی پاساژ) ⚠️:
  ردیابی ادغام بچ (Batch Traceability).
  هر ورودی می‌تواند از کاردینگ (source_type='carding')
  یا پاساژ قبلی (source_type='passage') باشد.
  این طراحی polymorphic تضمین می‌کند که زنجیره تولید
  از الیاف خام تا نخ نهایی قابل ردیابی است.
"""
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """تولید پاساژ - ادغام و کشش فتیله‌ها."""

    class PassageNumber(models.IntegerChoices):
        FIRST = 1, 'پاساژ اول'
        SECOND = 2, 'پاساژ دوم'

    # ── شماره پاساژ ─────────────────────────────────────
    passage_number = models.PositiveSmallIntegerField(
        choices=PassageNumber.choices,
        default=PassageNumber.FIRST,
        verbose_name='شماره پاساژ',
        help_text='۱=اول (ورودی از کاردینگ) | ۲=دوم (ورودی از پاساژ اول)',
    )

    # ── پارامترهای فنی (حیاتی) ──────────────────────────
    num_inputs = models.PositiveSmallIntegerField(
        default=6,
        verbose_name='تعداد فتیله ورودی',
        help_text='معمولاً ۶ تا ۸ فتیله',
    )
    draft_ratio = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name='نسبت کشش',
        help_text='مثلاً 6.500 یعنی ۶.۵ برابر',
    )
    output_sliver_count = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name='نمره فتیله خروجی',
    )
    output_weight_gperm = models.DecimalField(
        max_digits=8, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن فتیله خروجی (g/m)',
    )

    # ── وزن ──────────────────────────────────────────────
    input_total_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن کل ورودی (kg)',
    )
    output_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن خروجی (kg)',
    )

    # ── سرعت و کیفیت ────────────────────────────────────
    speed_mpm = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, null=True,
        verbose_name='سرعت (m/min)',
    )
    evenness_cv = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='CV% یکنواختی',
        help_text='ضریب تغییرات - مقدار کمتر بهتر (شاخص AI)',
    )

    class Meta:
        db_table = 'passage_production'
        verbose_name = 'تولید پاساژ'
        verbose_name_plural = 'تولیدات پاساژ'
        indexes = [
            models.Index(fields=['production_date'], name='idx_ps_date'),
            models.Index(fields=['passage_number'], name='idx_ps_number'),
        ]


class Input(models.Model):
    """
    ⚠️ ورودی‌های پاساژ - ردیابی ادغام بچ (Batch Traceability).
    
    هر ورودی مشخص می‌کند:
    - از کدام بچ کاردینگ یا پاساژ قبلی آمده (polymorphic)
    - در کدام جایگاه ورودی قرار گرفته (1 تا 8)
    - چقدر وزن مصرف شده
    """

    class SourceType(models.TextChoices):
        CARDING = 'carding', 'کاردینگ'
        PASSAGE = 'passage', 'پاساژ قبلی'

    passage_production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        verbose_name='بچ پاساژ',
        related_name='inputs',
    )
    input_position = models.PositiveSmallIntegerField(
        verbose_name='جایگاه ورودی',
        help_text='شماره ۱ تا ۸',
    )

    # ── منبع ورودی (Polymorphic) ─────────────────────────
    source_type = models.CharField(
        max_length=10,
        choices=SourceType.choices,
        verbose_name='نوع منبع',
    )
    source_id = models.BigIntegerField(
        verbose_name='شناسه منبع',
        help_text='ID بچ کاردینگ یا پاساژ',
    )
    source_batch_number = models.CharField(
        max_length=50,
        verbose_name='شماره بچ منبع',
        help_text='برای خوانایی سریع بدون JOIN',
    )

    weight_used = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن مصرفی (kg)',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت',
    )

    class Meta:
        db_table = 'passage_input'
        verbose_name = 'ورودی پاساژ'
        verbose_name_plural = 'ورودی‌های پاساژ'
        unique_together = [('passage_production', 'input_position')]
        indexes = [
            models.Index(fields=['source_type', 'source_id'], name='idx_pi_source'),
        ]

    def __str__(self):
        return f"جایگاه {self.input_position}: {self.source_batch_number} ({self.get_source_type_display()})"

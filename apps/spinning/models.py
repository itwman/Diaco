"""
Diaco MES - Spinning Models (رینگ)
====================================
مرحله نهایی تولید نخ: تبدیل فتیله به نخ با تاب و نمره مشخص.

منطق صنعتی:
───────────
Production (تولید رینگ):
  ورودی: فتیله از فینیشر.
  خروجی: نخ نهایی روی بوبین.
  پارامترهای کلیدی:
    - spindle_speed_rpm: سرعت دوک
    - twist_tpm: تاب نخ (دور بر متر) - تعیین‌کننده استحکام
    - twist_direction: جهت تاب (S یا Z)
    - yarn_count: نمره نخ نهایی
    - traveler_number: شماره شیطانک (قطعه مصرفی روی رینگ)
    - breakage_count: تعداد پارگی (شاخص کیفیت/AI)
    - efficiency_pct: راندمان = OEE (شاخص عملکرد/AI)

TravelerReplacement (تعویض شیطانک):
  شیطانک قطعه مصرفی است و باید دوره‌ای تعویض شود.
  next_due_at برای هشدار PM (نگهداری پیشگیرانه) استفاده می‌شود.
"""
from django.conf import settings
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """تولید رینگ - تبدیل فتیله به نخ."""

    class TwistDirection(models.TextChoices):
        S = 'S', 'S (چپ‌تاب)'
        Z = 'Z', 'Z (راست‌تاب)'

    # ── ارتباط با فینیشر ─────────────────────────────────
    finisher_production = models.ForeignKey(
        'finisher.Production',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='بچ فینیشر',
        related_name='spinning_productions',
    )

    # ── پارامترهای رینگ ─────────────────────────────────
    spindle_speed_rpm = models.IntegerField(
        verbose_name='سرعت دوک (RPM)',
    )
    twist_tpm = models.DecimalField(
        max_digits=8, decimal_places=2,
        verbose_name='تاب (TPM)',
        help_text='دور بر متر - تعیین‌کننده استحکام نخ',
    )
    twist_direction = models.CharField(
        max_length=1,
        choices=TwistDirection.choices,
        default=TwistDirection.Z,
        verbose_name='جهت تاب',
    )
    yarn_count = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name='نمره نخ نهایی',
    )

    # ── شیطانک ──────────────────────────────────────────
    traveler_number = models.CharField(
        max_length=20,
        blank=True, default='',
        verbose_name='شماره شیطانک',
    )
    traveler_type = models.CharField(
        max_length=50,
        blank=True, default='',
        verbose_name='نوع شیطانک',
    )
    ring_diameter = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True,
        verbose_name='قطر رینگ (mm)',
    )

    # ── وزن و تولید ─────────────────────────────────────
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
    num_spindles_active = models.IntegerField(
        blank=True, null=True,
        verbose_name='دوک فعال',
    )
    num_spindles_total = models.IntegerField(
        blank=True, null=True,
        verbose_name='دوک کل',
    )

    # ── کیفیت و عملکرد (AI) ─────────────────────────────
    breakage_count = models.IntegerField(
        default=0,
        verbose_name='تعداد پارگی',
        help_text='شاخص کیفیت - الگوی پارگی برای AI',
    )
    efficiency_pct = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='راندمان (%)',
        help_text='OEE - شاخص عملکرد برای AI',
    )

    class Meta:
        db_table = 'spinning_production'
        verbose_name = 'تولید رینگ'
        verbose_name_plural = 'تولیدات رینگ'
        indexes = [
            models.Index(fields=['production_date'], name='idx_sp_date'),
            models.Index(fields=['machine'], name='idx_sp_machine'),
        ]


class TravelerReplacement(models.Model):
    """سیکل تعویض شیطانک - برای هشدار PM."""

    class Reason(models.TextChoices):
        SCHEDULED = 'scheduled', 'برنامه‌ریزی شده'
        WORN = 'worn', 'فرسوده'
        BREAKAGE = 'breakage', 'شکستگی'
        QUALITY = 'quality', 'مشکل کیفی'

    machine = models.ForeignKey(
        'core.Machine',
        on_delete=models.CASCADE,
        verbose_name='ماشین',
        related_name='traveler_replacements',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='اپراتور',
        related_name='traveler_replacements',
    )
    replaced_at = models.DateTimeField(
        verbose_name='تاریخ تعویض',
    )
    old_traveler = models.CharField(
        max_length=50,
        blank=True, default='',
        verbose_name='شیطانک قدیم',
    )
    new_traveler = models.CharField(
        max_length=50,
        verbose_name='شیطانک جدید',
    )
    spindle_range = models.CharField(
        max_length=50,
        blank=True, default='',
        verbose_name='بازه دوک‌ها',
        help_text='مثال: 1-240',
    )
    reason = models.CharField(
        max_length=20,
        choices=Reason.choices,
        default=Reason.SCHEDULED,
        verbose_name='دلیل تعویض',
    )
    running_hours = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, null=True,
        verbose_name='ساعت کارکرد تا تعویض',
    )
    next_due_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name='تعویض بعدی',
        help_text='برای هشدار PM',
    )
    notes = models.TextField(
        blank=True, default='',
        verbose_name='یادداشت',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت',
    )

    class Meta:
        db_table = 'spinning_travelerreplacement'
        verbose_name = 'تعویض شیطانک'
        verbose_name_plural = 'تعویض شیطانک‌ها'
        ordering = ['-replaced_at']
        indexes = [
            models.Index(fields=['machine'], name='idx_tr_machine'),
            models.Index(fields=['next_due_at'], name='idx_tr_next_due'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.new_traveler} | {self.replaced_at}"

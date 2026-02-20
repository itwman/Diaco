"""
Diaco MES - Winding Models (بوبین‌پیچی)
=========================================
مرحله ششم خط تولید نخ فرش:
  انتقال نخ از بوبین‌های کوچک رینگ (Cop/Bobbin) به بوبین‌های بزرگ (Cone/Cheese/Package).

منطق صنعتی:
───────────
Production (تولید بوبین‌پیچی):
  ورودی: بوبین‌های کوچک (Cop) از رینگ
  خروجی: بوبین‌های بزرگ (Cone/Cheese) آماده برای دولاتابی
  اهمیت:
    - Yarn Clearer نقص‌های نخ (Thick/Thin/Nep) را در این مرحله حذف می‌کند
    - cuts_per_100km: هر برش = یک نقص نخ (شاخص کیفیت الیاف/رینگ)
    - splices_per_100km: تعداد اتصالات (باید کمتر از cuts باشد)
    - efficiency_pct: راندمان ماشین = (زمان واقعی تولید / زمان کل) × ۱۰۰
  استانداردهای صنعتی:
    - cuts_per_100km < 20 = کیفیت خوب
    - cuts_per_100km > 50 = مشکل در رینگ یا الیاف
    - efficiency_pct > 85% = قابل قبول

شماره‌گذاری: WD-YYMMDD-NNN (مثال: WD-041130-001)
"""
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """
    تولید بوبین‌پیچی.
    انتقال نخ از Cop رینگ به Cone/Package برای دولاتابی.
    """

    class PackageType(models.TextChoices):
        CONE = 'cone', 'کُن (Cone)'
        CHEESE = 'cheese', 'چیز (Cheese)'
        SPOOL = 'spool', 'اسپول (Spool)'

    # ── ارتباط با رینگ ───────────────────────────────────
    spinning_production = models.ForeignKey(
        'spinning.Production',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='بچ رینگ ورودی',
        related_name='winding_productions',
        help_text='بچ رینگی که نخ آن بوبین‌پیچی می‌شود',
    )

    # ── ورودی از رینگ ────────────────────────────────────
    input_cops = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='تعداد بوبین ورودی (Cop)',
        help_text='تعداد بوبین‌های کوچک رینگ',
    )
    input_weight_kg = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='وزن ورودی (kg)',
    )

    # ── پارامترهای ماشین ──────────────────────────────────
    winding_speed_mpm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='سرعت بوبین‌پیچی (m/min)',
        help_text='معمولاً ۸۰۰-۲۰۰۰ متر بر دقیقه',
    )
    tension_setting_cn = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='تنظیم کشش (cN)',
        help_text='Centi-Newton — کشش نخ روی ماشین',
    )
    yarn_clearer_type = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='نوع Yarn Clearer',
        help_text='مثال: Uster Quantum 4, Loepfe YarnMaster',
    )

    # ── بوبین‌های خروجی ───────────────────────────────────
    package_type = models.CharField(
        max_length=10,
        choices=PackageType.choices,
        default=PackageType.CONE,
        verbose_name='نوع بوبین خروجی',
    )
    package_weight_kg = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='وزن هر بوبین خروجی (kg)',
        help_text='وزن استاندارد هر Cone/Cheese',
    )
    output_packages = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='تعداد بوبین خروجی',
    )
    output_weight_kg = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='وزن خروجی کل (kg)',
    )

    # ── ضایعات ───────────────────────────────────────────
    waste_weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='ضایعات (kg)',
        help_text='نخ ابتدا/انتهای هر بوبین که دور ریخته می‌شود',
    )

    # ── شاخص‌های کیفیت (AI-Ready) ─────────────────────────
    cuts_per_100km = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='برش در ۱۰۰ کیلومتر',
        help_text='Cuts/100km — هر برش = یک نقص نخ. <20 خوب، >50 مشکل‌دار',
    )
    splices_per_100km = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='اتصال در ۱۰۰ کیلومتر',
        help_text='Splices/100km — تعداد پیوندهای انجام‌شده',
    )
    efficiency_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='راندمان (%)',
        help_text='درصد زمان مفید تولید — برای OEE',
    )

    class Meta:
        db_table = 'winding_production'
        verbose_name = 'تولید بوبین‌پیچی'
        verbose_name_plural = 'تولیدات بوبین‌پیچی'
        ordering = ['-production_date', '-created_at']
        indexes = [
            models.Index(fields=['production_date'], name='idx_wd_date'),
            models.Index(fields=['machine'], name='idx_wd_machine'),
            models.Index(fields=['status'], name='idx_wd_status'),
            models.Index(fields=['order'], name='idx_wd_order'),
        ]

    def __str__(self):
        return f"{self.batch_number} | {self.machine.code} | {self.get_status_display()}"

    @property
    def waste_pct(self):
        """درصد ضایعات"""
        if self.input_weight_kg and self.input_weight_kg > 0 and self.waste_weight_kg:
            return round(float(self.waste_weight_kg) / float(self.input_weight_kg) * 100, 2)
        return None

    @property
    def quality_grade(self):
        """درجه‌بندی کیفیت بر اساس cuts_per_100km"""
        if self.cuts_per_100km is None:
            return 'نامشخص'
        if self.cuts_per_100km < 20:
            return 'A - عالی'
        elif self.cuts_per_100km < 40:
            return 'B - خوب'
        elif self.cuts_per_100km < 60:
            return 'C - متوسط'
        return 'D - ضعیف'

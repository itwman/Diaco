"""
Diaco MES - TFO Models (دولاتابی Two-for-One Twisting)
=======================================================
مرحله هفتم خط تولید نخ فرش:
  تاباندن ۲ یا چند نخ تک‌لا به دور هم برای ساخت نخ دولا (Plied Yarn).

منطق صنعتی:
───────────
Production (تولید دولاتابی TFO):
  ورودی: بوبین‌های Cone از بوبین‌پیچی
  خروجی: بوبین‌های نخ دولا آماده برای هیت‌ست یا رنگرزی

  TFO = Two-for-One:
    هر دور دوک = ۲ تاب به نخ می‌دهد → سرعت ۲× نسبت به رینگ تابی سنتی

  در نخ فرش:
    - معمولاً ۲ رشته نخ با هم تاب می‌خورند (ply_count=2)
    - تاب نهایی باید در جهت مخالف تاب رینگ باشد:
        رینگ Z → TFO S  یا  رینگ S → TFO Z
    - twist_tpm نخ فرش: معمولاً ۱۵۰-۴۰۰ دور/متر

  شاخص‌های کیفی:
    - breakage_count کم = کیفیت الیاف و بوبین ورودی خوب
    - efficiency_pct > 90% قابل قبول برای TFO

شماره‌گذاری: TFO-YYMMDD-NNN (مثال: TFO-041130-001)
"""
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """
    تولید دولاتابی TFO.
    ترکیب چند نخ تک‌لا با تاب برای ساخت نخ دولا فرش.
    """

    class TwistDirection(models.TextChoices):
        S = 'S', 'S (چپ‌تاب)'
        Z = 'Z', 'Z (راست‌تاب)'

    # ── ارتباط با بوبین‌پیچی ─────────────────────────────
    winding_production = models.ForeignKey(
        'winding.Production',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='بچ بوبین‌پیچی ورودی',
        related_name='tfo_productions',
        help_text='بچ بوبین‌پیچی که نخ آن دولاتابی می‌شود',
    )

    # ── مشخصات نخ ────────────────────────────────────────
    ply_count = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='تعداد لا',
        help_text='تعداد نخ‌های ترکیب‌شده — معمولاً ۲ برای نخ فرش',
    )
    input_yarn_count_ne = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='نمره نخ ورودی (Ne)',
        help_text='نمره انگلیسی نخ تک‌لا ورودی',
    )
    output_yarn_count_ne = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='نمره نخ خروجی (Ne)',
        help_text='نمره نخ دولا = نمره ورودی / تعداد لا (تقریبی)',
    )

    # ── پارامترهای تاب ───────────────────────────────────
    twist_tpm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='تاب (TPM)',
        help_text='دور بر متر — نخ فرش: ۱۵۰-۴۰۰ TPM',
    )
    twist_direction = models.CharField(
        max_length=1,
        choices=TwistDirection.choices,
        default=TwistDirection.S,
        verbose_name='جهت تاب',
        help_text='باید مخالف جهت تاب رینگ باشد (رینگ Z → TFO S)',
    )
    spindle_speed_rpm = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='سرعت دوک (RPM)',
    )
    tension_weight_g = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='وزن تانسیون (g)',
        help_text='وزن تانسیون‌دهنده نخ',
    )
    balloon_control = models.BooleanField(
        default=False,
        verbose_name='کنترل بالون',
        help_text='آیا ماشین دارای کنترل بالون نخ است؟',
    )

    # ── تولید ────────────────────────────────────────────
    input_packages = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='تعداد بوبین ورودی',
    )
    input_weight_kg = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='وزن ورودی (kg)',
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
        verbose_name='وزن خروجی (kg)',
    )
    waste_weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='ضایعات (kg)',
    )

    # ── کیفیت و راندمان (AI-Ready) ───────────────────────
    breakage_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد پارگی',
        help_text='تعداد پارگی‌های نخ در طول تولید — شاخص کیفیت',
    )
    efficiency_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='راندمان (%)',
        help_text='درصد زمان مفید — برای OEE',
    )

    class Meta:
        db_table = 'tfo_production'
        verbose_name = 'تولید دولاتابی TFO'
        verbose_name_plural = 'تولیدات دولاتابی TFO'
        ordering = ['-production_date', '-created_at']
        indexes = [
            models.Index(fields=['production_date'], name='idx_tfo_date'),
            models.Index(fields=['machine'], name='idx_tfo_machine'),
            models.Index(fields=['status'], name='idx_tfo_status'),
            models.Index(fields=['order'], name='idx_tfo_order'),
        ]

    def __str__(self):
        return f"{self.batch_number} | {self.ply_count}لا | {self.twist_tpm}TPM | {self.get_status_display()}"

    @property
    def waste_pct(self):
        """درصد ضایعات"""
        if self.input_weight_kg and self.input_weight_kg > 0 and self.waste_weight_kg:
            return round(float(self.waste_weight_kg) / float(self.input_weight_kg) * 100, 2)
        return None

    @property
    def calculated_output_count(self):
        """نمره نخ خروجی تئوری = نمره ورودی / تعداد لا"""
        if self.input_yarn_count_ne and self.ply_count:
            return round(float(self.input_yarn_count_ne) / self.ply_count, 3)
        return None

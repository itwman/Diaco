"""
Diaco MES - HeatSet Models (هیت‌ست / تثبیت حرارتی)
====================================================
مرحله هشتم خط تولید نخ فرش:
  تثبیت تاب نخ دولا با بخار یا حرارت برای جلوگیری از چروک‌شدن در فرش.

منطق صنعتی:
───────────
Batch (بچ هیت‌ست):
  ورودی: بوبین‌های نخ دولا از TFO
  خروجی: نخ با تاب تثبیت‌شده آماده بافت

  چرا هیت‌ست ضروری است؟
    بدون هیت‌ست، تاب نخ در فرش آزاد می‌شود →
    نخ می‌پیچد → فرش چروک می‌شود و کیفیت بافت افت می‌کند.

  انواع رایج:
    - Autoclave: خلأ + بخار (۱۰۵-۱۲۵°C) — رایج‌ترین برای PA و پشم
    - Superba: پیوسته با بخار (۱۱۰-۱۳۵°C) — برای اکریلیک
    - Suessen: حرارت خشک (۱۳۰-۱۸۰°C) — برای پلی‌استر

  چرخه استاندارد Autoclave:
    پیش‌گرم → خلأ → تزریق بخار → نگه‌داری → خلأ نهایی → سردکردن

  پارامترهای بحرانی بر اساس نوع الیاف:
    پلی‌استر:  ۱۳۰-۱۸۰°C  (نیاز به دمای بالاتر)
    اکریلیک:   ۱۱۰-۱۳۵°C
    نایلون PA:  ۱۰۵-۱۲۵°C  (حساس به دما)
    پشم:        ۱۰۰-۱۲۰°C  (با احتیاط)

  نتایج کیفی:
    - shrinkage_pct: آنکاژ (کوچک‌شدن) — باید در محدوده استاندارد باشد
    - twist_stability: excellent/good/fair/poor

CycleLog (لاگ چرخه — AI-Ready):
  هر ۵ دقیقه یک رکورد از دما و فشار ذخیره می‌شود.
  این داده برای رسم منحنی چرخه و تحلیل AI استفاده می‌شود.

شماره‌گذاری: HS-YYMMDD-NNN (مثال: HS-041130-001)
"""
from datetime import datetime
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel


class Batch(TimeStampedModel):
    """
    بچ هیت‌ست — یک بار بارگذاری اتوکلاو یا عبور از خط پیوسته.
    """

    class MachineTypeHS(models.TextChoices):
        AUTOCLAVE = 'autoclave', 'اتوکلاو (Autoclave)'
        SUPERBA = 'superba', 'سوپربا (Superba) - پیوسته'
        SUESSEN = 'suessen', 'سوسن (Suessen) - حرارت خشک'
        OTHER = 'other', 'سایر'

    class FiberType(models.TextChoices):
        POLYESTER = 'polyester', 'پلی‌استر'
        ACRYLIC = 'acrylic', 'اکریلیک'
        WOOL = 'wool', 'پشم'
        NYLON = 'nylon', 'نایلون (PA)'
        POLYPROPYLENE = 'polypropylene', 'پلی‌پروپیلن'
        BLEND = 'blend', 'مخلوط'

    class CycleType(models.TextChoices):
        STANDARD = 'standard', 'استاندارد'
        INTENSIVE = 'intensive', 'فشرده (Intensive)'
        GENTLE = 'gentle', 'ملایم (Gentle)'

    class QualityResult(models.TextChoices):
        PASS = 'pass', 'قبول ✓'
        FAIL = 'fail', 'رد ✗'
        CONDITIONAL = 'conditional', 'مشروط'

    class TwistStability(models.TextChoices):
        EXCELLENT = 'excellent', 'عالی'
        GOOD = 'good', 'خوب'
        FAIR = 'fair', 'متوسط'
        POOR = 'poor', 'ضعیف'

    class BatchStatus(models.TextChoices):
        LOADING = 'loading', 'در حال بارگذاری'
        PROCESSING = 'processing', 'در حال فرآیند'
        COOLING = 'cooling', 'در حال سردشدن'
        COMPLETED = 'completed', 'تکمیل شده'
        FAILED = 'failed', 'ناموفق'

    # ── شناسه ────────────────────────────────────────────
    batch_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='شماره بچ',
        help_text='HS-YYMMDD-NNN',
    )

    # ── ارتباطات ─────────────────────────────────────────
    tfo_production = models.ForeignKey(
        'tfo.Production',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='بچ TFO ورودی',
        related_name='heatset_batches',
        help_text='بچ دولاتابی که هیت‌ست می‌شود',
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='سفارش',
        related_name='heatset_batches',
    )
    machine = models.ForeignKey(
        'core.Machine',
        on_delete=models.PROTECT,
        verbose_name='ماشین هیت‌ست',
        related_name='heatset_batches',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='اپراتور',
        related_name='heatset_batches',
    )
    shift = models.ForeignKey(
        'core.Shift',
        on_delete=models.PROTECT,
        verbose_name='شیفت',
        related_name='heatset_batches',
    )
    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='heatset_batches',
    )
    production_date = models.DateField(
        verbose_name='تاریخ تولید',
    )

    # ── مشخصات ماشین و نوع فرآیند ────────────────────────
    machine_type_hs = models.CharField(
        max_length=15,
        choices=MachineTypeHS.choices,
        default=MachineTypeHS.AUTOCLAVE,
        verbose_name='نوع دستگاه هیت‌ست',
    )
    fiber_type = models.CharField(
        max_length=15,
        choices=FiberType.choices,
        default=FiberType.POLYESTER,
        verbose_name='نوع الیاف',
        help_text='برای تنظیم دما و زمان چرخه',
    )
    cycle_type = models.CharField(
        max_length=15,
        choices=CycleType.choices,
        default=CycleType.STANDARD,
        verbose_name='نوع چرخه',
    )

    # ── پارامترهای حرارتی ─────────────────────────────────
    temperature_c = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='دمای تثبیت (°C)',
        help_text='PA: 105-125 | اکریلیک: 110-135 | پلی‌استر: 130-180',
    )
    steam_pressure_bar = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='فشار بخار (bar)',
        help_text='برای Autoclave — معمولاً ۱.۲-۲.۵ bar',
    )
    vacuum_level_mbar = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='سطح خلأ (mbar)',
        help_text='برای Autoclave — معمولاً ۵۰-۱۵۰ mbar',
    )
    humidity_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='رطوبت محفظه (%)',
    )

    # ── زمان‌بندی چرخه (دقیقه) ────────────────────────────
    pre_heat_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='پیش‌گرم (دقیقه)',
    )
    vacuum_time_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='خلأ (دقیقه)',
    )
    steam_time_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='تزریق بخار (دقیقه)',
    )
    dwell_time_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='نگه‌داری (دقیقه)',
    )
    cooldown_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='سردشدن (دقیقه)',
    )
    duration_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='مدت کل (دقیقه)',
        help_text='جمع کل مراحل — محاسبه خودکار',
    )

    # ── بارگذاری ─────────────────────────────────────────
    batch_weight_kg = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='وزن بچ (kg)',
        help_text='وزن کل نخ در این بار هیت‌ست',
    )
    packages_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='تعداد بوبین',
    )

    # ── نتایج کیفی ────────────────────────────────────────
    quality_result = models.CharField(
        max_length=15,
        choices=QualityResult.choices,
        blank=True,
        null=True,
        verbose_name='نتیجه کیفی',
        db_index=True,
    )
    shrinkage_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='آنکاژ / کوچک‌شدن (%)',
        help_text='درصد کاهش وزن/طول نخ پس از هیت‌ست',
    )
    twist_stability = models.CharField(
        max_length=15,
        choices=TwistStability.choices,
        blank=True,
        null=True,
        verbose_name='پایداری تاب',
    )

    # ── وضعیت ────────────────────────────────────────────
    status = models.CharField(
        max_length=15,
        choices=BatchStatus.choices,
        default=BatchStatus.LOADING,
        verbose_name='وضعیت',
        db_index=True,
    )
    started_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='شروع',
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='پایان',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )

    # ── AI-Ready ─────────────────────────────────────────
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='متادیتا (AI)',
        help_text='داده‌های کامل چرخه برای تحلیل AI',
    )

    class Meta:
        db_table = 'heatset_batch'
        verbose_name = 'بچ هیت‌ست'
        verbose_name_plural = 'بچ‌های هیت‌ست'
        ordering = ['-production_date', '-created_at']
        indexes = [
            models.Index(fields=['production_date'], name='idx_hs_date'),
            models.Index(fields=['machine'], name='idx_hs_machine'),
            models.Index(fields=['status'], name='idx_hs_status'),
            models.Index(fields=['quality_result'], name='idx_hs_quality'),
            models.Index(fields=['order'], name='idx_hs_order'),
        ]

    def __str__(self):
        return f"{self.batch_number} | {self.temperature_c}°C | {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """محاسبه خودکار مدت کل چرخه"""
        total = 0
        for field in ['pre_heat_min', 'vacuum_time_min', 'steam_time_min', 'dwell_time_min', 'cooldown_min']:
            val = getattr(self, field)
            if val:
                total += val
        if total > 0:
            self.duration_min = total
        super().save(*args, **kwargs)

    @property
    def is_passed(self):
        return self.quality_result == 'pass'


class CycleLog(models.Model):
    """
    لاگ لحظه‌ای چرخه هیت‌ست — AI-Ready Time Series Data.
    هر ۵ دقیقه یک رکورد از دما، فشار و مرحله ذخیره می‌شود.
    این داده برای:
      - رسم نمودار منحنی چرخه در داشبورد
      - مقایسه چرخه‌های مختلف
      - تحلیل AI (اگر منحنی دمایی غیرعادی باشد → هشدار)
    """

    class Phase(models.TextChoices):
        PREHEAT = 'preheat', 'پیش‌گرم'
        VACUUM = 'vacuum', 'خلأ'
        STEAM = 'steam', 'تزریق بخار'
        DWELL = 'dwell', 'نگه‌داری'
        COOLDOWN = 'cooldown', 'سردشدن'

    heatset_batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        verbose_name='بچ هیت‌ست',
        related_name='cycle_logs',
    )
    log_time = models.DateTimeField(
        default=datetime.now,
        verbose_name='زمان ثبت',
    )
    elapsed_min = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='دقیقه از شروع',
    )
    # پارامترهای لحظه‌ای
    temperature_c = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='دمای لحظه‌ای (°C)',
    )
    pressure_bar = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name='فشار لحظه‌ای (bar)',
    )
    humidity_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='رطوبت لحظه‌ای (%)',
    )
    phase = models.CharField(
        max_length=10,
        choices=Phase.choices,
        verbose_name='مرحله فرآیند',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت',
    )

    class Meta:
        db_table = 'heatset_cyclelog'
        verbose_name = 'لاگ چرخه هیت‌ست'
        verbose_name_plural = 'لاگ‌های چرخه هیت‌ست'
        ordering = ['heatset_batch', 'log_time']
        indexes = [
            models.Index(fields=['heatset_batch'], name='idx_cl_batch'),
            models.Index(fields=['heatset_batch', 'log_time'], name='idx_cl_batch_time'),
        ]

    def __str__(self):
        return f"{self.heatset_batch.batch_number} | {self.get_phase_display()} | {self.temperature_c}°C"

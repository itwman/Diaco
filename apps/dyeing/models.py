"""
Diaco MES - Dyeing Models (رنگرزی)
=====================================
واحد رنگرزی: رنگ‌آمیزی الیاف/نخ + دیگ بخار + خشک‌کن.

منطق صنعتی:
───────────
Batch (بچ رنگرزی):
  هر بچ یک شید رنگی (ColorShade) مشخص دارد.
  پارامترها: نسبت حمام، دما، pH، مدت زمان.
  وضعیت: preparation → in_progress → cooling → drying → completed/failed

ChemicalUsage (مصرف مواد):
  ثبت دقیق مواد مصرفی (رنگ + شیمیایی) در هر بچ.
  ترتیب اضافه‌کردن مواد (sequence_order) مهم است.

BoilerLog (دیگ بخار):
  ثبت روزانه فشار، دما، سطح آب، مصرف سوخت.

DryerLog (خشک‌کن):
  ثبت دما، مدت و رطوبت خروجی برای هر بچ.
"""
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel
from apps.inventory.models import DyeStock, ChemicalStock


# ═══════════════════════════════════════════════════════════════
# DYEING BATCH (بچ رنگرزی)
# ═══════════════════════════════════════════════════════════════

class Batch(TimeStampedModel):
    """بچ رنگرزی - فرآیند رنگ‌آمیزی الیاف یا نخ."""

    class Status(models.TextChoices):
        PREPARATION = 'preparation', 'آماده‌سازی'
        IN_PROGRESS = 'in_progress', 'در حال رنگرزی'
        COOLING = 'cooling', 'خنک‌سازی'
        DRYING = 'drying', 'خشک‌کردن'
        COMPLETED = 'completed', 'تکمیل شده'
        FAILED = 'failed', 'ناموفق'

    class QualityResult(models.TextChoices):
        PASS = 'pass', 'قبول'
        FAIL = 'fail', 'مردود'
        CONDITIONAL = 'conditional', 'مشروط'

    # ── شناسه ────────────────────────────────────────────
    batch_number = models.CharField(
        max_length=50, unique=True,
        verbose_name='شماره بچ',
    )

    # ── ارتباطات ─────────────────────────────────────────
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='سفارش',
        related_name='dyeing_batches',
    )
    color_shade = models.ForeignKey(
        'orders.ColorShade',
        on_delete=models.PROTECT,
        verbose_name='شید رنگی',
        related_name='dyeing_batches',
    )
    machine = models.ForeignKey(
        'core.Machine',
        on_delete=models.PROTECT,
        verbose_name='دیگ رنگرزی',
        related_name='dyeing_batches',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='اپراتور',
        related_name='dyeing_batches',
    )
    shift = models.ForeignKey(
        'core.Shift',
        on_delete=models.PROTECT,
        verbose_name='شیفت',
        related_name='dyeing_batches',
    )
    production_date = models.DateField(
        verbose_name='تاریخ تولید',
    )

    # ── پارامترهای رنگرزی ───────────────────────────────
    fiber_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='وزن الیاف (kg)',
    )
    liquor_ratio = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='نسبت حمام',
        help_text='مثلاً 1:8',
    )
    temperature = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='دمای حمام (°C)',
    )
    duration_min = models.IntegerField(
        blank=True, null=True,
        verbose_name='مدت زمان (دقیقه)',
    )
    ph_value = models.DecimalField(
        max_digits=4, decimal_places=2,
        blank=True, null=True,
        verbose_name='pH',
    )

    # ── وضعیت ───────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PREPARATION,
        verbose_name='وضعیت',
        db_index=True,
    )
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='شروع')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='پایان')
    quality_result = models.CharField(
        max_length=15,
        choices=QualityResult.choices,
        blank=True, default='',
        verbose_name='نتیجه کیفیت',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    metadata = models.JSONField(blank=True, null=True, default=dict, verbose_name='متادیتا (AI)')

    class Meta:
        db_table = 'dyeing_batch'
        verbose_name = 'بچ رنگرزی'
        verbose_name_plural = 'بچ‌های رنگرزی'
        ordering = ['-production_date']
        indexes = [
            models.Index(fields=['production_date'], name='idx_dy_date'),
        ]

    def __str__(self):
        return f"{self.batch_number} | {self.color_shade.code} | {self.get_status_display()}"


# ═══════════════════════════════════════════════════════════════
# CHEMICAL USAGE (مصرف مواد)
# ═══════════════════════════════════════════════════════════════

class ChemicalUsage(models.Model):
    """مصرف مواد شیمیایی و رنگ در هر بچ رنگرزی."""

    class MaterialType(models.TextChoices):
        DYE = 'dye', 'رنگ'
        CHEMICAL = 'chemical', 'ماده شیمیایی'

    dyeing_batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        verbose_name='بچ رنگرزی',
        related_name='chemical_usages',
    )
    material_type = models.CharField(
        max_length=10,
        choices=MaterialType.choices,
        verbose_name='نوع ماده',
    )
    dye_stock = models.ForeignKey(
        DyeStock,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name='رنگ مصرفی',
        related_name='dyeing_usages',
    )
    chemical_stock = models.ForeignKey(
        ChemicalStock,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name='ماده شیمیایی مصرفی',
        related_name='dyeing_usages',
    )
    quantity_used = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='مقدار مصرفی',
    )
    unit = models.CharField(max_length=10, verbose_name='واحد')
    step_name = models.CharField(
        max_length=100,
        blank=True, default='',
        verbose_name='مرحله مصرف',
        help_text='مثال: شست‌وشو، رنگرزی، تثبیت',
    )
    sequence_order = models.PositiveSmallIntegerField(
        blank=True, null=True,
        verbose_name='ترتیب اضافه‌کردن',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        db_table = 'dyeing_chemicalusage'
        verbose_name = 'مصرف مواد رنگرزی'
        verbose_name_plural = 'مصرف مواد رنگرزی'
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.get_material_type_display()} | {self.quantity_used} {self.unit}"


# ═══════════════════════════════════════════════════════════════
# BOILER LOG (دیگ بخار)
# ═══════════════════════════════════════════════════════════════

class BoilerLog(models.Model):
    """لاگ روزانه دیگ بخار."""

    class Status(models.TextChoices):
        RUNNING = 'running', 'در حال کار'
        IDLE = 'idle', 'خاموش'
        MAINTENANCE = 'maintenance', 'در حال تعمیر'

    machine = models.ForeignKey(
        'core.Machine', on_delete=models.PROTECT,
        verbose_name='دیگ بخار', related_name='boiler_logs',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='اپراتور', related_name='boiler_logs',
    )
    shift = models.ForeignKey(
        'core.Shift', on_delete=models.PROTECT,
        verbose_name='شیفت', related_name='boiler_logs',
    )
    log_date = models.DateField(verbose_name='تاریخ')

    # ── پارامترها ───────────────────────────────────────
    pressure_bar = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, verbose_name='فشار (bar)',
    )
    temperature_c = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, verbose_name='دما (°C)',
    )
    water_level = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True, verbose_name='سطح آب (%)',
    )
    fuel_consumed = models.DecimalField(
        max_digits=10, decimal_places=3,
        blank=True, null=True, verbose_name='مصرف سوخت',
    )
    running_hours = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, verbose_name='ساعت کار',
    )
    status = models.CharField(
        max_length=15, choices=Status.choices,
        default=Status.RUNNING, verbose_name='وضعیت',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    metadata = models.JSONField(blank=True, null=True, default=dict, verbose_name='متادیتا (AI)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        db_table = 'dyeing_boilerlog'
        verbose_name = 'لاگ دیگ بخار'
        verbose_name_plural = 'لاگ‌های دیگ بخار'
        ordering = ['-log_date']
        indexes = [
            models.Index(fields=['machine', 'log_date'], name='idx_boiler_machine_date'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.log_date} | {self.get_status_display()}"


# ═══════════════════════════════════════════════════════════════
# DRYER LOG (خشک‌کن)
# ═══════════════════════════════════════════════════════════════

class DryerLog(models.Model):
    """لاگ خشک‌کن."""

    class Status(models.TextChoices):
        RUNNING = 'running', 'در حال کار'
        IDLE = 'idle', 'خاموش'
        MAINTENANCE = 'maintenance', 'در حال تعمیر'

    machine = models.ForeignKey(
        'core.Machine', on_delete=models.PROTECT,
        verbose_name='خشک‌کن', related_name='dryer_logs',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='اپراتور', related_name='dryer_logs',
    )
    shift = models.ForeignKey(
        'core.Shift', on_delete=models.PROTECT,
        verbose_name='شیفت', related_name='dryer_logs',
    )
    dyeing_batch = models.ForeignKey(
        Batch, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='بچ رنگرزی', related_name='dryer_logs',
    )
    log_date = models.DateField(verbose_name='تاریخ')

    # ── پارامترها ───────────────────────────────────────
    temperature_c = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True, verbose_name='دما (°C)',
    )
    duration_min = models.IntegerField(
        blank=True, null=True, verbose_name='مدت (دقیقه)',
    )
    humidity_pct = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True, verbose_name='رطوبت خروجی (%)',
    )
    status = models.CharField(
        max_length=15, choices=Status.choices,
        default=Status.RUNNING, verbose_name='وضعیت',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    metadata = models.JSONField(blank=True, null=True, default=dict, verbose_name='متادیتا (AI)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        db_table = 'dyeing_dryerlog'
        verbose_name = 'لاگ خشک‌کن'
        verbose_name_plural = 'لاگ‌های خشک‌کن'
        ordering = ['-log_date']
        indexes = [
            models.Index(fields=['machine', 'log_date'], name='idx_dryer_machine_date'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.log_date} | {self.get_status_display()}"

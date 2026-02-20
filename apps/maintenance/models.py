"""
Diaco MES - Maintenance Models (نگهداری و تعمیرات)
=====================================================
سیستم نگهداری پیشگیرانه (PM) و ثبت توقفات.

منطق صنعتی:
───────────
Schedule (برنامه سرویس):
  هر ماشین برنامه PM دارد: روزانه، هفتگی، ماهانه و ...
  next_due_at برای هشدار خودکار. اگر گذشته باشد → overdue.

WorkOrder (دستور کار):
  هر تعمیر یک WO دارد. می‌تواند از PM (preventive)
  یا خرابی (corrective/emergency) باشد.
  ثبت هزینه قطعات + دستمزد.

DowntimeLog (لاگ توقف):
  هر توقف ماشین با دلیل و مدت ثبت می‌شود.
  reason_category برای تحلیل آماری و AI.
  production_loss: تولید از دست رفته.

MachineServiceDate (تاریخ سرویس):
  سوابق سرویس‌های انجام‌شده + قطعات تعویضی.
"""
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel


# ═══════════════════════════════════════════════════════════════
# SCHEDULE (برنامه سرویس)
# ═══════════════════════════════════════════════════════════════

class Schedule(TimeStampedModel):
    """برنامه نگهداری پیشگیرانه (PM)."""

    class MaintenanceType(models.TextChoices):
        PREVENTIVE = 'preventive', 'پیشگیرانه'
        CORRECTIVE = 'corrective', 'اصلاحی'
        PREDICTIVE = 'predictive', 'پیش‌بینانه'
        OVERHAUL = 'overhaul', 'اساسی'

    class Frequency(models.TextChoices):
        DAILY = 'daily', 'روزانه'
        WEEKLY = 'weekly', 'هفتگی'
        BIWEEKLY = 'biweekly', 'دو هفته‌ای'
        MONTHLY = 'monthly', 'ماهانه'
        QUARTERLY = 'quarterly', 'سه‌ماهه'
        SEMI_ANNUAL = 'semi_annual', 'شش‌ماهه'
        ANNUAL = 'annual', 'سالانه'
        CUSTOM = 'custom', 'سفارشی'

    class Priority(models.TextChoices):
        LOW = 'low', 'کم'
        MEDIUM = 'medium', 'متوسط'
        HIGH = 'high', 'بالا'
        CRITICAL = 'critical', 'بحرانی'

    machine = models.ForeignKey(
        'core.Machine', on_delete=models.CASCADE,
        verbose_name='ماشین', related_name='maintenance_schedules',
    )
    maintenance_type = models.CharField(
        max_length=15, choices=MaintenanceType.choices,
        verbose_name='نوع نگهداری',
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(blank=True, default='', verbose_name='شرح')
    frequency = models.CharField(
        max_length=15, choices=Frequency.choices,
        verbose_name='دوره تکرار',
    )
    custom_days = models.IntegerField(
        blank=True, null=True,
        verbose_name='تعداد روز (سفارشی)',
    )
    last_done_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name='آخرین انجام',
    )
    next_due_at = models.DateTimeField(
        verbose_name='موعد بعدی',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='مسئول', related_name='assigned_schedules',
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices,
        default=Priority.MEDIUM, verbose_name='اولویت',
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        db_table = 'maintenance_schedule'
        verbose_name = 'برنامه سرویس'
        verbose_name_plural = 'برنامه‌های سرویس'
        ordering = ['next_due_at']
        indexes = [
            models.Index(fields=['next_due_at'], name='idx_mnt_next_due'),
            models.Index(fields=['machine'], name='idx_mnt_machine'),
            models.Index(fields=['is_active', 'next_due_at'], name='idx_mnt_overdue'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.title} | {self.get_frequency_display()}"

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.is_active and self.next_due_at < timezone.now()


# ═══════════════════════════════════════════════════════════════
# WORK ORDER (دستور کار)
# ═══════════════════════════════════════════════════════════════

class WorkOrder(TimeStampedModel):
    """دستور کار تعمیرات."""

    class WOType(models.TextChoices):
        PREVENTIVE = 'preventive', 'پیشگیرانه'
        CORRECTIVE = 'corrective', 'اصلاحی'
        EMERGENCY = 'emergency', 'اضطراری'

    class Priority(models.TextChoices):
        LOW = 'low', 'کم'
        MEDIUM = 'medium', 'متوسط'
        HIGH = 'high', 'بالا'
        CRITICAL = 'critical', 'بحرانی'

    class Status(models.TextChoices):
        OPEN = 'open', 'باز'
        IN_PROGRESS = 'in_progress', 'در حال انجام'
        WAITING_PARTS = 'waiting_parts', 'در انتظار قطعات'
        COMPLETED = 'completed', 'تکمیل شده'
        CANCELLED = 'cancelled', 'لغو شده'

    wo_number = models.CharField(
        max_length=20, unique=True,
        verbose_name='شماره دستور کار',
        help_text='فرمت: WO-YYYYMMDD-NNN',
    )
    schedule = models.ForeignKey(
        Schedule, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='برنامه PM', related_name='work_orders',
    )
    machine = models.ForeignKey(
        'core.Machine', on_delete=models.PROTECT,
        verbose_name='ماشین', related_name='work_orders',
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(blank=True, default='', verbose_name='شرح')
    wo_type = models.CharField(
        max_length=15, choices=WOType.choices,
        verbose_name='نوع',
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices,
        default=Priority.MEDIUM, verbose_name='اولویت',
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='گزارش‌دهنده', related_name='reported_workorders',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='مسئول اجرا', related_name='assigned_workorders',
    )
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.OPEN, verbose_name='وضعیت', db_index=True,
    )
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='شروع')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='پایان')
    downtime_min = models.IntegerField(blank=True, null=True, verbose_name='مدت توقف (دقیقه)')
    cost_parts = models.DecimalField(
        max_digits=15, decimal_places=0,
        default=0, verbose_name='هزینه قطعات (ریال)',
    )
    cost_labor = models.DecimalField(
        max_digits=15, decimal_places=0,
        default=0, verbose_name='هزینه دستمزد (ریال)',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')

    class Meta:
        db_table = 'maintenance_workorder'
        verbose_name = 'دستور کار'
        verbose_name_plural = 'دستورهای کار'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['machine'], name='idx_wo_machine'),
            models.Index(fields=['priority', 'status'], name='idx_wo_prio_status'),
        ]

    def __str__(self):
        return f"{self.wo_number} | {self.machine.code} | {self.get_status_display()}"

    @property
    def total_cost(self):
        return self.cost_parts + self.cost_labor


# ═══════════════════════════════════════════════════════════════
# DOWNTIME LOG (لاگ توقفات)
# ═══════════════════════════════════════════════════════════════

class DowntimeLog(models.Model):
    """لاگ توقفات ماشین‌آلات."""

    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='downtime_logs',
    )

    class ReasonCategory(models.TextChoices):
        MECHANICAL = 'mechanical', 'مکانیکی'
        ELECTRICAL = 'electrical', 'برقی'
        MATERIAL = 'material', 'مواد اولیه'
        OPERATOR = 'operator', 'اپراتور'
        QUALITY = 'quality', 'کیفیت'
        PLANNED = 'planned', 'برنامه‌ریزی شده'
        OTHER = 'other', 'سایر'

    machine = models.ForeignKey(
        'core.Machine', on_delete=models.PROTECT,
        verbose_name='ماشین', related_name='downtime_logs',
    )
    work_order = models.ForeignKey(
        WorkOrder, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='دستور کار', related_name='downtime_logs',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='اپراتور', related_name='downtime_logs',
    )
    shift = models.ForeignKey(
        'core.Shift', on_delete=models.PROTECT,
        verbose_name='شیفت', related_name='downtime_logs',
    )
    start_time = models.DateTimeField(verbose_name='شروع توقف')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='پایان توقف')
    duration_min = models.IntegerField(blank=True, null=True, verbose_name='مدت (دقیقه)')
    reason_category = models.CharField(
        max_length=15, choices=ReasonCategory.choices,
        verbose_name='دسته‌بندی دلیل',
    )
    reason_detail = models.CharField(max_length=500, verbose_name='جزئیات دلیل')
    production_loss = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='تولید از دست رفته (kg)',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    metadata = models.JSONField(blank=True, null=True, default=dict, verbose_name='متادیتا (AI)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        db_table = 'maintenance_downtimelog'
        verbose_name = 'لاگ توقف'
        verbose_name_plural = 'لاگ‌های توقف'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['machine', 'start_time'], name='idx_dt_machine_date'),
            models.Index(fields=['reason_category'], name='idx_dt_reason'),
            models.Index(fields=['shift', 'start_time'], name='idx_dt_shift'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.get_reason_category_display()} | {self.duration_min} دقیقه"


# ═══════════════════════════════════════════════════════════════
# MACHINE SERVICE DATE (سوابق سرویس)
# ═══════════════════════════════════════════════════════════════

class MachineServiceDate(models.Model):
    """سوابق سرویس‌های انجام‌شده روی ماشین‌آلات."""

    machine = models.ForeignKey(
        'core.Machine', on_delete=models.CASCADE,
        verbose_name='ماشین', related_name='service_dates',
    )
    service_type = models.CharField(max_length=100, verbose_name='نوع سرویس')
    service_date = models.DateField(verbose_name='تاریخ سرویس')
    next_service = models.DateField(blank=True, null=True, verbose_name='سرویس بعدی')
    performed_by = models.CharField(
        max_length=200, blank=True, default='',
        verbose_name='سرویس‌کار',
    )
    cost = models.DecimalField(
        max_digits=15, decimal_places=0,
        default=0, verbose_name='هزینه (ریال)',
    )
    parts_replaced = models.JSONField(
        blank=True, null=True, default=dict,
        verbose_name='قطعات تعویض شده',
    )
    notes = models.TextField(blank=True, default='', verbose_name='یادداشت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        db_table = 'maintenance_machineservicedate'
        verbose_name = 'سابقه سرویس'
        verbose_name_plural = 'سوابق سرویس'
        ordering = ['-service_date']
        indexes = [
            models.Index(fields=['machine', 'service_date'], name='idx_svc_machine_date'),
            models.Index(fields=['next_service'], name='idx_svc_next'),
        ]

    def __str__(self):
        return f"{self.machine.code} | {self.service_type} | {self.service_date}"

"""
Diaco MES - Core Models
=========================
مدل‌های هسته‌ای که توسط تمام ماژول‌های تولیدی استفاده می‌شوند.

منطق صنعتی:
───────────
Machine (ماشین):
  هر ماشین در کارخانه یک کد منحصربفرد دارد (مثلاً CR-01 = کارد شماره ۱).
  نوع ماشین تعیین می‌کند در کدام مرحله تولید استفاده می‌شود.
  فیلد specs (JSON) برای ذخیره مشخصات فنی و داده‌های سنسوری آینده (AI) است.

Shift (شیفت):
  کارخانه‌های ریسندگی معمولاً ۳ شیفت ۸ ساعته دارند:
  صبح (A): 06:00-14:00 | عصر (B): 14:00-22:00 | شب (C): 22:00-06:00
  هر رکورد تولید به یک شیفت متصل است تا تحلیل عملکرد شیفتی ممکن شود.

AuditLog (لاگ تغییرات):
  هر تغییر در داده‌های حساس (تولید، انبار) ثبت می‌شود.
  این برای ردیابی و حسابرسی ضروری است.

Notification (اعلان):
  هشدارهای PM (نگهداری)، موجودی کم، توقف ماشین و غیره.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


# ═══════════════════════════════════════════════════════════════
# ABSTRACT BASE MODEL
# ═══════════════════════════════════════════════════════════════

class TimeStampedModel(models.Model):
    """
    مدل پایه با فیلدهای زمانی.
    تمام مدل‌های پروژه از این ارث‌بری می‌کنند.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی',
    )

    class Meta:
        abstract = True


# ═══════════════════════════════════════════════════════════════
# PRODUCTION BASE MODEL (مدل پایه تولید)
# ═══════════════════════════════════════════════════════════════

class ProductionBaseModel(TimeStampedModel):
    """
    مدل پایه برای تمام جداول تولیدی.
    فیلدهای مشترک: ماشین، اپراتور، شیفت، تاریخ، وضعیت، metadata.
    """

    class ProductionStatus(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'در حال تولید'
        COMPLETED = 'completed', 'تکمیل شده'
        QUALITY_HOLD = 'quality_hold', 'توقف کیفی'
        CANCELLED = 'cancelled', 'لغو شده'

    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='%(app_label)s_%(class)s_set',
    )
    batch_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='شماره بچ',
    )
    machine = models.ForeignKey(
        'core.Machine',
        on_delete=models.PROTECT,
        verbose_name='ماشین',
        related_name='%(app_label)s_%(class)s_set',
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='اپراتور',
        related_name='%(app_label)s_%(class)s_set',
    )
    shift = models.ForeignKey(
        'core.Shift',
        on_delete=models.PROTECT,
        verbose_name='شیفت',
        related_name='%(app_label)s_%(class)s_set',
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='سفارش',
        related_name='%(app_label)s_%(class)s_set',
    )
    production_date = models.DateField(
        verbose_name='تاریخ تولید',
    )
    status = models.CharField(
        max_length=20,
        choices=ProductionStatus.choices,
        default=ProductionStatus.IN_PROGRESS,
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
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='متادیتا (AI)',
        help_text='داده‌های سنسوری و تحلیلی',
    )

    class Meta:
        abstract = True
        ordering = ['-production_date', '-created_at']

    def __str__(self):
        return f"{self.batch_number} | {self.machine.code} | {self.get_status_display()}"


# ═══════════════════════════════════════════════════════════════
# PRODUCTION LINE (خط تولید)
# ═══════════════════════════════════════════════════════════════

class ProductionLine(TimeStampedModel):
    """
    خط تولید.
    یک کارخانه می‌تواند چند خط تولید مستقل داشته باشد.
    هر خط تولید:
      - ماشین‌آلات خاص خودش
      - شیفت‌ها و سرشیفت‌های خودش
      - محصولات خاص خودش
      - ظرفیت و کیفیت مستقل
    """

    class LineStatus(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        INACTIVE = 'inactive', 'غیرفعال'
        MAINTENANCE = 'maintenance', 'در حال تعمیر'

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد خط',
        help_text='مثال: LINE-01, LINE-02',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='نام خط تولید',
        help_text='مثال: خط یک - نخ پنبه‌ای',
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='توضیحات',
    )
    status = models.CharField(
        max_length=20,
        choices=LineStatus.choices,
        default=LineStatus.ACTIVE,
        verbose_name='وضعیت',
        db_index=True,
    )

    # ── محصول ────────────────────────────────────────
    product_type = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='نوع محصول',
        help_text='مثال: نخ پنبه Ne30، نخ مخلوط PES/VIS',
    )
    target_capacity_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='ظرفیت هدف (کیلو/شیفت)',
    )

    # ── مدیر خط ─────────────────────────────────────
    line_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='مدیر خط',
        related_name='managed_lines',
    )

    # ── AI-Ready ─────────────────────────────────────
    specs = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='مشخصات خط',
        help_text='ظرفیت، سرعت، محدودیت‌ها (JSON)',
    )

    class Meta:
        db_table = 'core_production_line'
        verbose_name = 'خط تولید'
        verbose_name_plural = 'خطوط تولید'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def machine_count(self):
        return self.machines.filter(status='active').count()

    @property
    def is_operational(self):
        return self.status == self.LineStatus.ACTIVE


# ═══════════════════════════════════════════════════════════════
# MACHINE (ماشین‌آلات)
# ═══════════════════════════════════════════════════════════════

class Machine(TimeStampedModel):
    """
    ماشین‌آلات کارخانه.
    هر ماشین با کد منحصربفرد شناسایی می‌شود.
    نوع ماشین تعیین‌کننده مرحله تولیدی آن است.
    """

    class MachineType(models.TextChoices):
        BLOWROOM = 'blowroom', 'حلاجی'
        CARDING = 'carding', 'کاردینگ'
        PASSAGE = 'passage', 'پاساژ / کشش'
        FINISHER = 'finisher', 'فینیشر'
        RING = 'ring', 'رینگ'
        # ── v2.0 خط تولید نخ فرش ────────────────────────
        WINDING = 'winding', 'بوبین‌پیچی'
        TFO = 'tfo', 'دولاتابی (TFO)'
        HEATSET = 'heatset', 'هیت‌ست'
        # ────────────────────────────────────────────────
        DYEING = 'dyeing', 'دستگاه رنگرزی'
        BOILER = 'boiler', 'دیگ بخار'
        DRYER = 'dryer', 'خشک‌کن'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        INACTIVE = 'inactive', 'غیرفعال'
        MAINTENANCE = 'maintenance', 'در حال تعمیر'
        DECOMMISSIONED = 'decommissioned', 'از رده خارج'

    # ── خط تولید ───────────────────────────────────────
    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='machines',
        help_text='خط تولیدی که این ماشین به آن اختصاص دارد',
    )

    # ── شناسه‌ها ─────────────────────────────────────────
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد ماشین',
        help_text='مثال: CR-01, RG-15, BL-02',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='نام ماشین',
        help_text='مثال: کارد شماره ۱، رینگ سالن ب',
    )

    # ── نوع و وضعیت ─────────────────────────────────────
    machine_type = models.CharField(
        max_length=20,
        choices=MachineType.choices,
        verbose_name='نوع ماشین',
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='وضعیت',
        db_index=True,
    )

    # ── مشخصات ──────────────────────────────────────────
    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='سازنده',
    )
    model_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='مدل',
    )
    year_installed = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='سال نصب',
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='محل استقرار',
        help_text='مثال: سالن الف، طبقه ۲',
    )

    # ── AI-Ready ────────────────────────────────────────
    specs = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='مشخصات فنی',
        help_text='مشخصات فنی ماشین به صورت JSON (برای تحلیل AI)',
    )

    class Meta:
        db_table = 'core_machine'
        verbose_name = 'ماشین'
        verbose_name_plural = 'ماشین‌آلات'
        ordering = ['machine_type', 'code']
        indexes = [
            models.Index(fields=['machine_type', 'status'], name='idx_machine_type_status'),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def is_operational(self):
        """آیا ماشین عملیاتی است؟"""
        return self.status == self.Status.ACTIVE


# ═══════════════════════════════════════════════════════════════
# SHIFT (شیفت کاری)
# ═══════════════════════════════════════════════════════════════

class Shift(models.Model):
    """
    شیفت‌های کاری کارخانه.
    معمولاً ۳ شیفت: صبح (A)، عصر (B)، شب (C).
    هر رکورد تولیدی به یک شیفت متصل است.
    """

    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='shifts',
        help_text='خالی = شیفت عمومی برای همه خطوط',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='نام شیفت',
        help_text='مثال: صبح، عصر، شب',
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد شیفت',
        help_text='مثال: L1-A, L1-B, L2-A',
    )
    start_time = models.TimeField(
        verbose_name='ساعت شروع',
    )
    end_time = models.TimeField(
        verbose_name='ساعت پایان',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    class Meta:
        db_table = 'core_shift'
        verbose_name = 'شیفت'
        verbose_name_plural = 'شیفت‌ها'
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.code}) | {self.start_time:%H:%M}-{self.end_time:%H:%M}"

    @property
    def duration_hours(self):
        """مدت شیفت به ساعت"""
        from datetime import datetime, timedelta
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        if end < start:
            end += timedelta(days=1)
        return (end - start).total_seconds() / 3600


# ═══════════════════════════════════════════════════════════════
# LINE SHIFT ASSIGNMENT (اختصاص سرشیفت به خط)
# ═══════════════════════════════════════════════════════════════

class LineShiftAssignment(models.Model):
    """
    اختصاص سرشیفت به هر خط/شیفت.
    مثال: خط ۱ + شیفت صبح → سرشیفت: علی محمدی
    """
    production_line = models.ForeignKey(
        ProductionLine,
        on_delete=models.CASCADE,
        verbose_name='خط تولید',
        related_name='shift_assignments',
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        verbose_name='شیفت',
        related_name='line_assignments',
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='سرشیفت',
        related_name='shift_supervisions',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    class Meta:
        db_table = 'core_line_shift_assignment'
        verbose_name = 'اختصاص سرشیفت'
        verbose_name_plural = 'اختصاص‌های سرشیفت'
        unique_together = ['production_line', 'shift']

    def __str__(self):
        return f"{self.production_line.code} | {self.shift.name} → {self.supervisor or '-'}"


# ═══════════════════════════════════════════════════════════════
# AUDIT LOG (لاگ تغییرات)
# ═══════════════════════════════════════════════════════════════

class AuditLog(models.Model):
    """
    لاگ تغییرات برای ردیابی و حسابرسی.
    هر تغییر مهم در سیستم اینجا ثبت می‌شود.
    """

    class Action(models.TextChoices):
        CREATE = 'create', 'ایجاد'
        UPDATE = 'update', 'ویرایش'
        DELETE = 'delete', 'حذف'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='کاربر',
        related_name='audit_logs',
    )
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        verbose_name='عملیات',
    )
    table_name = models.CharField(
        max_length=100,
        verbose_name='نام جدول',
    )
    record_id = models.BigIntegerField(
        verbose_name='شناسه رکورد',
    )
    old_values = models.JSONField(
        blank=True,
        null=True,
        verbose_name='مقادیر قبلی',
    )
    new_values = models.JSONField(
        blank=True,
        null=True,
        verbose_name='مقادیر جدید',
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='آدرس IP',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ',
    )

    class Meta:
        db_table = 'core_auditlog'
        verbose_name = 'لاگ تغییرات'
        verbose_name_plural = 'لاگ تغییرات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['table_name', 'record_id'], name='idx_audit_table_record'),
            models.Index(fields=['user'], name='idx_audit_user'),
            models.Index(fields=['-created_at'], name='idx_audit_created'),
        ]

    def __str__(self):
        return f"{self.get_action_display()} {self.table_name}#{self.record_id} توسط {self.user}"


# ═══════════════════════════════════════════════════════════════
# NOTIFICATION (اعلان‌ها)
# ═══════════════════════════════════════════════════════════════

class Notification(models.Model):
    """
    سیستم اعلان برای هشدارهای PM، موجودی، توقف و غیره.
    """

    class NotifType(models.TextChoices):
        INFO = 'info', 'اطلاعات'
        WARNING = 'warning', 'هشدار'
        DANGER = 'danger', 'خطر'
        SUCCESS = 'success', 'موفقیت'
        MAINTENANCE = 'maintenance', 'نگهداری'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='گیرنده',
        related_name='notifications',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان',
    )
    message = models.TextField(
        verbose_name='پیام',
    )
    notif_type = models.CharField(
        max_length=15,
        choices=NotifType.choices,
        default=NotifType.INFO,
        verbose_name='نوع',
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='خوانده شده',
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='لینک',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ',
    )

    class Meta:
        db_table = 'core_notification'
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read'], name='idx_notif_recipient_read'),
            models.Index(fields=['-created_at'], name='idx_notif_created'),
        ]

    def __str__(self):
        status = '✓' if self.is_read else '●'
        return f"{status} {self.title} → {self.recipient}"

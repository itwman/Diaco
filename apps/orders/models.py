"""
Diaco MES - Orders Models
============================
مدیریت سفارشات، مشتریان و فرآیند تأیید رنگ.

منطق صنعتی:
───────────
Customer (مشتری):
  هر مشتری سقف اعتبار (credit_limit) دارد.
  سفارشات بالاتر از سقف نیاز به تأیید مالی دارند.

ColorShade (شِید رنگی):
  هر رنگ سفارشی یک کد شید یکتا دارد (مثال: SH-1024).
  فرمول رنگ (recipe) به صورت JSON ذخیره می‌شود
  تا نسبت مواد شیمیایی و رنگ دقیقاً مشخص باشد.
  قبل از تولید انبوه، نمونه رنگ باید توسط مشتری تأیید شود.

ColorApprovalHistory (تاریخچه تأیید رنگ):
  فرآیند رفت‌وبرگشت نمونه رنگ:
  submitted → customer_review → approved/rejected/revised
  هر مرحله با تصویر نمونه و بازخورد مشتری ثبت می‌شود.

Order (سفارش):
  سفارش مشتری شامل نوع نخ، نمره، مقدار و تاریخ تحویل.
  اولویت‌بندی: low/normal/high/urgent
  وضعیت: draft → confirmed → in_production → quality_check → ready → delivered
  progress_pct (0-100) پیشرفت تولید را نشان می‌دهد.
"""
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel


# ═══════════════════════════════════════════════════════════════
# CUSTOMER (مشتریان)
# ═══════════════════════════════════════════════════════════════

class Customer(TimeStampedModel):
    """
    مشتریان کارخانه.
    شامل اطلاعات تماس، آدرس و سقف اعتبار.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='نام مشتری',
    )
    company = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='شرکت',
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        default='',
        verbose_name='تلفن',
    )
    mobile = models.CharField(
        max_length=15,
        blank=True,
        default='',
        verbose_name='موبایل',
    )
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='ایمیل',
    )
    address = models.TextField(
        blank=True,
        default='',
        verbose_name='آدرس',
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='شهر',
    )
    province = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='استان',
    )
    tax_id = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='شناسه مالیاتی',
    )
    credit_limit = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        default=0,
        verbose_name='سقف اعتبار (ریال)',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )

    class Meta:
        db_table = 'orders_customer'
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'
        ordering = ['name']

    def __str__(self):
        if self.company:
            return f"{self.name} ({self.company})"
        return self.name


# ═══════════════════════════════════════════════════════════════
# COLOR SHADE (شِید رنگی)
# ═══════════════════════════════════════════════════════════════

class ColorShade(TimeStampedModel):
    """
    شِید رنگی: هر رنگ سفارشی یک کد و فرمول مشخص دارد.
    فرمول به صورت JSON ذخیره می‌شود تا نسبت مواد دقیق باشد.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='کد شید',
        help_text='مثال: SH-1024',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='نام رنگ',
    )
    color_hex = models.CharField(
        max_length=7,
        blank=True,
        default='',
        verbose_name='کد رنگ HEX',
        help_text='مثال: #FF5733',
    )
    recipe = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='فرمول رنگ',
        help_text='نسبت مواد شیمیایی و رنگ به صورت JSON',
    )
    image = models.ImageField(
        upload_to='color_shades/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='تصویر نمونه',
    )

    # ── تأیید ───────────────────────────────────────────
    is_approved = models.BooleanField(
        default=False,
        verbose_name='تأیید شده',
        db_index=True,
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='تأیید توسط',
        related_name='approved_shades',
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ تأیید',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )

    class Meta:
        db_table = 'orders_colorshade'
        verbose_name = 'شید رنگی'
        verbose_name_plural = 'شیدهای رنگی'
        ordering = ['code']

    def __str__(self):
        status = '✓' if self.is_approved else '○'
        return f"{status} {self.code} - {self.name}"

    def color_preview(self):
        """نمایش پیش‌نمایش رنگ"""
        if self.color_hex:
            from django.utils.html import format_html
            return format_html(
                '<span style="display:inline-block; width:20px; height:20px; '
                'background:{}; border:1px solid #ccc; border-radius:3px;"></span>',
                self.color_hex
            )
        return '-'


# ═══════════════════════════════════════════════════════════════
# COLOR APPROVAL HISTORY (تاریخچه تأیید رنگ)
# ═══════════════════════════════════════════════════════════════

class ColorApprovalHistory(models.Model):
    """
    تاریخچه فرآیند تأیید رنگ توسط مشتری.
    هر نمونه ارسالی و بازخورد مشتری ثبت می‌شود.
    """

    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'ارسال شده'
        CUSTOMER_REVIEW = 'customer_review', 'در بررسی مشتری'
        APPROVED = 'approved', 'تأیید شده'
        REJECTED = 'rejected', 'رد شده'
        REVISED = 'revised', 'اصلاح شده'

    color_shade = models.ForeignKey(
        ColorShade,
        on_delete=models.CASCADE,
        verbose_name='شید رنگی',
        related_name='approval_history',
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='مشتری',
        related_name='color_approvals',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name='وضعیت',
    )
    sample_image = models.ImageField(
        upload_to='color_samples/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='تصویر نمونه ارسالی',
    )
    customer_feedback = models.TextField(
        blank=True,
        default='',
        verbose_name='بازخورد مشتری',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='بررسی توسط',
        related_name='color_reviews',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ',
    )

    class Meta:
        db_table = 'orders_colorapprovalhistory'
        verbose_name = 'تاریخچه تأیید رنگ'
        verbose_name_plural = 'تاریخچه تأیید رنگ'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['color_shade', 'status'], name='idx_shade_status'),
        ]

    def __str__(self):
        return f"{self.color_shade.code} → {self.customer.name}: {self.get_status_display()}"


# ═══════════════════════════════════════════════════════════════
# ORDER (سفارش)
# ═══════════════════════════════════════════════════════════════

class Order(TimeStampedModel):
    """
    سفارش مشتری.
    هر سفارش شامل نوع نخ، مقدار، تاریخ تحویل و وضعیت پیشرفت.
    """

    class Priority(models.TextChoices):
        LOW = 'low', 'کم'
        NORMAL = 'normal', 'عادی'
        HIGH = 'high', 'بالا'
        URGENT = 'urgent', 'فوری'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'پیش‌نویس'
        SAMPLE_SENT = 'sample_sent', 'نمونه ارسال شد'
        CUSTOMER_APPROVED = 'customer_approved', 'تأیید مشتری'
        CONFIRMED = 'confirmed', 'تأیید شده'
        IN_PRODUCTION = 'in_production', 'در حال تولید'
        QUALITY_CHECK = 'quality_check', 'کنترل کیفیت'
        READY = 'ready', 'آماده تحویل'
        DELIVERED = 'delivered', 'تحویل داده شده'
        CANCELLED = 'cancelled', 'لغو شده'

    # ── شناسه ────────────────────────────────────────────
    order_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='شماره سفارش',
        help_text='فرمت: ORD-YYYYMMDD-NNN',
    )

    # ── ارتباطات ─────────────────────────────────────────
    production_line = models.ForeignKey(
        'core.ProductionLine',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='خط تولید',
        related_name='orders',
        help_text='خطی که این سفارش روی آن تولید می‌شود',
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name='مشتری',
        related_name='orders',
    )
    color_shade = models.ForeignKey(
        ColorShade,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='شید رنگی',
        related_name='orders',
    )

    # ── مشخصات نخ ────────────────────────────────────────
    yarn_type = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='نوع نخ',
    )
    yarn_count = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='نمره نخ',
        help_text='مثال: Ne 30/1',
    )
    quantity_kg = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار (kg)',
    )

    # ── مالی ─────────────────────────────────────────────
    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='قیمت واحد (ریال)',
    )
    total_price = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='مبلغ کل (ریال)',
    )

    # ── زمان‌بندی و اولویت ───────────────────────────────
    delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ تحویل',
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
        verbose_name='اولویت',
    )

    # ── وضعیت و پیشرفت ──────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='وضعیت',
        db_index=True,
    )
    progress_pct = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='پیشرفت (%)',
        help_text='۰ تا ۱۰۰',
    )

    # ── ایجادکننده ───────────────────────────────────────
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='ایجاد توسط',
        related_name='created_orders',
    )
    # ── مشخصات نخ فرش (v2.0) ────────────────────────────

    class ProcessSequence(models.TextChoices):
        NO_DYE = 'no_dye', 'بدون رنگرزی'
        PRE_DYE = 'pre_dye', 'رنگرزی قبل از هیت‌ست'
        POST_DYE = 'post_dye', 'رنگرزی بعد از هیت‌ست'
        STOCK_DYE = 'stock_dye', 'رنگرزی الیاف (Stock Dyeing)'

    ply_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='تعداد لا',
        help_text='۱=تک‌لا، ۲=دولا (معمولاً برای نخ فرش)',
    )
    heatset_required = models.BooleanField(
        default=False,
        verbose_name='نیاز به هیت‌ست',
        help_text='آیا نخ باید هیت‌ست شود؟',
    )
    process_sequence = models.CharField(
        max_length=20,
        choices=ProcessSequence.choices,
        default=ProcessSequence.NO_DYE,
        verbose_name='ترتیب فرآیند',
        help_text='آیا رنگرزی قبل، بعد یا بدون هیت‌ست انجام شود؟',
    )

    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )

    class Meta:
        db_table = 'orders_order'
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer'], name='idx_order_customer'),
            models.Index(fields=['status'], name='idx_order_status'),
            models.Index(fields=['delivery_date'], name='idx_order_delivery'),
            models.Index(fields=['priority', 'status'], name='idx_order_prio_status'),
        ]

    def __str__(self):
        return f"{self.order_number} | {self.customer.name} | {self.get_status_display()}"

    @property
    def is_overdue(self):
        """آیا تحویل عقب‌افتاده؟ — بدون timezone (سازگار با USE_TZ=False)"""
        if self.delivery_date and self.status not in ('delivered', 'cancelled'):
            from datetime import date
            return self.delivery_date < date.today()
        return False

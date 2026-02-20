"""
Diaco MES - Inventory Models
===============================
مدیریت انبار مواد اولیه کارخانه ریسندگی.

منطق صنعتی:
───────────
FiberCategory (دسته‌بندی الیاف):
  انواع الیاف مصرفی: پلی‌استر، اکریلیک، پشم، ویسکوز و ...
  هر الیاف دسته‌بندی مشخصی دارد.

FiberStock (موجودی الیاف):
  هر بسته الیاف با batch_number یکتا وارد انبار می‌شود.
  مصرف بر اساس FIFO (اول وارد، اول مصرف) از روی received_date.
  current_weight با هر مصرف در حلاجی کاهش می‌یابد.
  quality_grade (A/B/C) تأثیر مستقیم بر کیفیت نخ نهایی دارد.

DyeStock (موجودی رنگ):
  رنگ‌های مصرفی در واحد رنگرزی.
  انواع: reactive, disperse, acid, vat, direct.

ChemicalStock (مواد شیمیایی):
  اسید، قلیا، نمک، نرم‌کننده و سایر مواد کمکی رنگرزی.
  فیلد concentration (غلظت) برای محاسبه دقیق فرمول رنگ.

StockTransaction (تراکنش انبار):
  هر ورود/خروج/برگشت/تعدیل/ضایعات ثبت می‌شود.
  ارتباط polymorphic: هم نوع موجودی (fiber/dye/chemical) و هم
  مرجع مصرف (blowroom_batch, dyeing_batch) ثبت می‌شود.
"""
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel


# ═══════════════════════════════════════════════════════════════
# FIBER CATEGORY (دسته‌بندی الیاف)
# ═══════════════════════════════════════════════════════════════

class FiberCategory(models.Model):
    """
    دسته‌بندی الیاف مصرفی.
    مثال: پلی‌استر، اکریلیک، پشم، ویسکوز، نایلون.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='نام دسته',
        help_text='مثال: پلی‌استر، اکریلیک، پشم',
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد',
        help_text='مثال: PES, ACR, WOL',
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='توضیحات',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    class Meta:
        db_table = 'inventory_fibercategory'
        verbose_name = 'دسته‌بندی الیاف'
        verbose_name_plural = 'دسته‌بندی الیاف'
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ═══════════════════════════════════════════════════════════════
# FIBER STOCK (موجودی الیاف)
# ═══════════════════════════════════════════════════════════════

class FiberStock(TimeStampedModel):
    """
    موجودی الیاف خام در انبار.
    هر بسته با batch_number یکتا ردیابی می‌شود.
    مصرف بر اساس FIFO از روی received_date.
    """

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'موجود'
        RESERVED = 'reserved', 'رزرو شده'
        CONSUMED = 'consumed', 'مصرف شده'
        RETURNED = 'returned', 'برگشتی'

    class QualityGrade(models.TextChoices):
        A = 'A', 'درجه یک'
        B = 'B', 'درجه دو'
        C = 'C', 'درجه سه'

    # ── ارتباط دسته‌بندی ─────────────────────────────────
    category = models.ForeignKey(
        FiberCategory,
        on_delete=models.PROTECT,
        verbose_name='دسته‌بندی',
        related_name='stocks',
    )

    # ── شناسه‌های بچ ─────────────────────────────────────
    batch_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='شماره بچ',
        help_text='شماره بچ/لات منحصربفرد',
    )
    lot_number = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='شماره لات تأمین‌کننده',
    )

    # ── اطلاعات تأمین‌کننده ──────────────────────────────
    supplier = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='تأمین‌کننده',
    )
    color_raw = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='رنگ اولیه',
        help_text='رنگ الیاف خام (سفید، اکرو و ...)',
    )

    # ── مشخصات فنی ───────────────────────────────────────
    denier = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='دنیر',
        help_text='ضخامت الیاف (دنیر)',
    )
    staple_length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='طول الیاف (mm)',
    )

    # ── وزن ──────────────────────────────────────────────
    initial_weight = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='وزن اولیه (kg)',
    )
    current_weight = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='وزن فعلی (kg)',
    )

    # ── مالی ─────────────────────────────────────────────
    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='قیمت واحد (ریال)',
    )

    # ── تاریخ‌ها ────────────────────────────────────────
    received_date = models.DateField(
        verbose_name='تاریخ ورود',
        help_text='کلید FIFO: اول وارد، اول مصرف',
    )
    expiry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ انقضا',
    )

    # ── انبارداری ────────────────────────────────────────
    warehouse_loc = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='محل انبار',
        help_text='مثال: ردیف ۳ - قفسه ب',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        verbose_name='وضعیت',
        db_index=True,
    )
    quality_grade = models.CharField(
        max_length=1,
        choices=QualityGrade.choices,
        default=QualityGrade.A,
        verbose_name='درجه کیفیت',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )

    class Meta:
        db_table = 'inventory_fiberstock'
        verbose_name = 'موجودی الیاف'
        verbose_name_plural = 'موجودی الیاف'
        ordering = ['received_date']
        indexes = [
            models.Index(fields=['status', 'received_date'], name='idx_fiber_fifo'),
            models.Index(fields=['category'], name='idx_fiber_category'),
        ]

    def __str__(self):
        return f"{self.batch_number} | {self.category.name} | {self.current_weight}kg"

    @property
    def consumed_weight(self):
        """وزن مصرف‌شده"""
        return self.initial_weight - self.current_weight

    @property
    def consumed_pct(self):
        """درصد مصرف"""
        if self.initial_weight > 0:
            return round((self.consumed_weight / self.initial_weight) * 100, 1)
        return 0


# ═══════════════════════════════════════════════════════════════
# DYE STOCK (موجودی رنگ)
# ═══════════════════════════════════════════════════════════════

class DyeStock(TimeStampedModel):
    """
    موجودی رنگ‌های مصرفی در واحد رنگرزی.
    هر رنگ با کد یکتا شناسایی می‌شود.
    """

    class DyeType(models.TextChoices):
        REACTIVE = 'reactive', 'راکتیو'
        DISPERSE = 'disperse', 'دیسپرس'
        ACID = 'acid', 'اسیدی'
        VAT = 'vat', 'خمی'
        DIRECT = 'direct', 'مستقیم'

    class Unit(models.TextChoices):
        KG = 'kg', 'کیلوگرم'
        G = 'g', 'گرم'
        LITER = 'liter', 'لیتر'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'موجود'
        RESERVED = 'reserved', 'رزرو شده'
        CONSUMED = 'consumed', 'مصرف شده'
        EXPIRED = 'expired', 'منقضی'

    # ── شناسه‌ها ─────────────────────────────────────────
    name = models.CharField(
        max_length=200,
        verbose_name='نام رنگ',
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='کد رنگ',
    )
    color_family = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='خانواده رنگ',
        help_text='مثال: قرمز، آبی، سبز',
    )

    # ── مشخصات ──────────────────────────────────────────
    dye_type = models.CharField(
        max_length=20,
        choices=DyeType.choices,
        verbose_name='نوع رنگ',
        db_index=True,
    )
    manufacturer = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='سازنده',
    )
    batch_number = models.CharField(
        max_length=50,
        verbose_name='شماره بچ',
    )

    # ── وزن ──────────────────────────────────────────────
    initial_weight = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار اولیه',
    )
    current_weight = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار فعلی',
    )
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.KG,
        verbose_name='واحد',
    )

    # ── مالی ─────────────────────────────────────────────
    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='قیمت واحد (ریال)',
    )

    # ── تاریخ‌ها ────────────────────────────────────────
    received_date = models.DateField(
        verbose_name='تاریخ ورود',
    )
    expiry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ انقضا',
    )

    # ── نگهداری ─────────────────────────────────────────
    storage_temp = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='دمای نگهداری (°C)',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        verbose_name='وضعیت',
    )

    class Meta:
        db_table = 'inventory_dyestock'
        verbose_name = 'موجودی رنگ'
        verbose_name_plural = 'موجودی رنگ'
        ordering = ['received_date']
        indexes = [
            models.Index(fields=['status', 'received_date'], name='idx_dye_status_date'),
            models.Index(fields=['dye_type'], name='idx_dye_type'),
        ]

    def __str__(self):
        return f"{self.code} - {self.name} | {self.current_weight}{self.unit}"


# ═══════════════════════════════════════════════════════════════
# CHEMICAL STOCK (مواد شیمیایی)
# ═══════════════════════════════════════════════════════════════

class ChemicalStock(TimeStampedModel):
    """
    موجودی مواد شیمیایی کمکی رنگرزی.
    اسید، قلیا، نمک، نرم‌کننده، تثبیت‌کننده و ...
    """

    class ChemicalType(models.TextChoices):
        ACID = 'acid', 'اسید'
        ALKALI = 'alkali', 'قلیا'
        SALT = 'salt', 'نمک'
        SOFTENER = 'softener', 'نرم‌کننده'
        FIXATIVE = 'fixative', 'تثبیت‌کننده'
        AUXILIARY = 'auxiliary', 'کمکی'
        OTHER = 'other', 'سایر'

    class Unit(models.TextChoices):
        KG = 'kg', 'کیلوگرم'
        G = 'g', 'گرم'
        LITER = 'liter', 'لیتر'
        ML = 'ml', 'میلی‌لیتر'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'موجود'
        RESERVED = 'reserved', 'رزرو شده'
        CONSUMED = 'consumed', 'مصرف شده'
        EXPIRED = 'expired', 'منقضی'

    # ── شناسه‌ها ─────────────────────────────────────────
    name = models.CharField(
        max_length=200,
        verbose_name='نام ماده',
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='کد',
    )

    # ── مشخصات ──────────────────────────────────────────
    chemical_type = models.CharField(
        max_length=20,
        choices=ChemicalType.choices,
        verbose_name='نوع ماده',
        db_index=True,
    )
    manufacturer = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='سازنده',
    )
    batch_number = models.CharField(
        max_length=50,
        verbose_name='شماره بچ',
    )

    # ── مقدار ────────────────────────────────────────────
    initial_amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار اولیه',
    )
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار فعلی',
    )
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.KG,
        verbose_name='واحد',
    )
    concentration = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='غلظت (%)',
    )

    # ── مالی ─────────────────────────────────────────────
    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='قیمت واحد (ریال)',
    )

    # ── تاریخ‌ها ────────────────────────────────────────
    received_date = models.DateField(
        verbose_name='تاریخ ورود',
    )
    expiry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ انقضا',
    )

    # ── ایمنی ───────────────────────────────────────────
    msds_file = models.FileField(
        upload_to='msds/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='برگه ایمنی (MSDS)',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        verbose_name='وضعیت',
    )

    class Meta:
        db_table = 'inventory_chemicalstock'
        verbose_name = 'موجودی مواد شیمیایی'
        verbose_name_plural = 'موجودی مواد شیمیایی'
        ordering = ['received_date']
        indexes = [
            models.Index(fields=['status', 'received_date'], name='idx_chem_status_date'),
            models.Index(fields=['chemical_type'], name='idx_chemical_type'),
        ]

    def __str__(self):
        return f"{self.code} - {self.name} | {self.current_amount}{self.unit}"


# ═══════════════════════════════════════════════════════════════
# STOCK TRANSACTION (تراکنش انبار)
# ═══════════════════════════════════════════════════════════════

class StockTransaction(models.Model):
    """
    تراکنش‌های انبار: ورود، خروج، برگشت، تعدیل، ضایعات.
    ارتباط Polymorphic:
      - stock_type + stock_id → به کدام موجودی مربوط است
      - reference_type + reference_id → مرجع مصرف (کدام بچ تولید)
    """

    class StockType(models.TextChoices):
        FIBER = 'fiber', 'الیاف'
        DYE = 'dye', 'رنگ'
        CHEMICAL = 'chemical', 'مواد شیمیایی'

    class TransactionType(models.TextChoices):
        RECEIVE = 'receive', 'ورود به انبار'
        ISSUE = 'issue', 'خروج از انبار'
        RETURN = 'return', 'برگشت به انبار'
        ADJUST = 'adjust', 'تعدیل موجودی'
        WASTE = 'waste', 'ضایعات'

    # ── مرجع موجودی (Polymorphic) ─────────────────────────
    stock_type = models.CharField(
        max_length=20,
        choices=StockType.choices,
        verbose_name='نوع موجودی',
    )
    stock_id = models.BigIntegerField(
        verbose_name='شناسه موجودی',
    )

    # ── نوع تراکنش ──────────────────────────────────────
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name='نوع تراکنش',
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='مقدار',
    )
    unit = models.CharField(
        max_length=10,
        verbose_name='واحد',
    )

    # ── مرجع مصرف (Polymorphic) ──────────────────────────
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='نوع مرجع',
        help_text='مثال: blowroom_batch, dyeing_batch',
    )
    reference_id = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name='شناسه مرجع',
    )

    # ── ثبت‌کننده ────────────────────────────────────────
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='انجام‌دهنده',
        related_name='stock_transactions',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='یادداشت',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ تراکنش',
    )

    class Meta:
        db_table = 'inventory_stocktransaction'
        verbose_name = 'تراکنش انبار'
        verbose_name_plural = 'تراکنش‌های انبار'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stock_type', 'stock_id'], name='idx_stock_ref'),
            models.Index(fields=['reference_type', 'reference_id'], name='idx_txn_reference'),
            models.Index(fields=['-created_at'], name='idx_txn_created'),
        ]

    def __str__(self):
        return f"{self.get_transaction_type_display()} | {self.get_stock_type_display()} | {self.quantity} {self.unit}"

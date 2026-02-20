"""
Diaco MES - Accounts Models
==============================
مدل کاربر سفارشی برای سیستم MES ریسندگی.

منطق صنعتی:
- در کارخانه ریسندگی ۴ سطح دسترسی وجود دارد:
  * admin: مدیر سیستم (دسترسی کامل)
  * manager: مدیر تولید (مشاهده + گزارش + ویرایش)
  * supervisor: سرپرست سالن (ثبت تولید + مشاهده)
  * operator: اپراتور ماشین (فقط ثبت داده تولید)
  * viewer: بازرس / ناظر (فقط مشاهده)

- هر کاربر به یک بخش (department) تعلق دارد.
- کد ملی به عنوان شناسه منحصربفرد انسانی استفاده می‌شود.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر سفارشی دیاکو MES.
    از AbstractBaseUser ارث‌بری می‌کند تا کنترل کامل داشته باشیم.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'مدیر سیستم'
        MANAGER = 'manager', 'مدیر تولید'
        SUPERVISOR = 'supervisor', 'سرپرست'
        OPERATOR = 'operator', 'اپراتور'
        VIEWER = 'viewer', 'ناظر'

    class Department(models.TextChoices):
        PRODUCTION = 'production', 'تولید'
        WAREHOUSE = 'warehouse', 'انبار'
        DYEING = 'dyeing', 'رنگرزی'
        MAINTENANCE = 'maintenance', 'نگهداری و تعمیرات'
        QUALITY = 'quality', 'کنترل کیفیت'
        OFFICE = 'office', 'اداری'

    # ── شناسه‌ها ─────────────────────────────────────────
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='نام کاربری',
        help_text='نام کاربری برای ورود به سیستم',
        error_messages={
            'unique': 'کاربری با این نام قبلاً ثبت شده است.',
        },
    )

    # ── اطلاعات شخصی ────────────────────────────────────
    first_name = models.CharField(
        max_length=100,
        verbose_name='نام',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی',
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name='کد ملی',
        help_text='کد ملی ۱۰ رقمی',
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        default='',
        verbose_name='تلفن',
    )
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='ایمیل',
    )

    # ── نقش و بخش ───────────────────────────────────────
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OPERATOR,
        verbose_name='نقش',
        db_index=True,
    )
    department = models.CharField(
        max_length=20,
        choices=Department.choices,
        default=Department.PRODUCTION,
        verbose_name='بخش',
        db_index=True,
    )

    # ── وضعیت ───────────────────────────────────────────
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='دسترسی پنل مدیریت',
    )

    # ── آواتار ──────────────────────────────────────────
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='تصویر پروفایل',
    )

    # ── تاریخ‌ها ────────────────────────────────────────
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='تاریخ عضویت',
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='آخرین ورود',
    )

    # ── مدیر ────────────────────────────────────────────
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role'], name='idx_user_role'),
            models.Index(fields=['department'], name='idx_user_dept'),
            models.Index(fields=['is_active'], name='idx_user_active'),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        """نام کامل فارسی"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_manager(self):
        return self.role in (self.Role.ADMIN, self.Role.MANAGER)

    @property
    def is_supervisor(self):
        return self.role in (self.Role.ADMIN, self.Role.MANAGER, self.Role.SUPERVISOR)

    @property
    def can_edit_production(self):
        """آیا می‌تواند داده تولید ثبت/ویرایش کند؟"""
        return self.role in (
            self.Role.ADMIN, self.Role.MANAGER,
            self.Role.SUPERVISOR, self.Role.OPERATOR,
        )

    @property
    def can_view_reports(self):
        """آیا می‌تواند گزارش‌ها را ببیند؟"""
        return self.role != self.Role.OPERATOR

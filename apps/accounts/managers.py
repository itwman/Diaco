"""
Diaco MES - Custom User Manager
=================================
منطق ساخت کاربر عادی و ادمین.
در کارخانه ریسندگی، اپراتور فقط با کد ملی و رمز وارد می‌شود.
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    مدیر سفارشی کاربر دیاکو.
    از username به جای email به عنوان شناسه اصلی استفاده می‌کند
    چون اپراتورهای کارخانه معمولاً ایمیل ندارند.
    """

    def create_user(self, username, password=None, **extra_fields):
        """ساخت کاربر عادی (اپراتور/سرپرست)"""
        if not username:
            raise ValueError('نام کاربری الزامی است.')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'operator')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """ساخت ابرکاربر (مدیر سیستم)"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('ابرکاربر باید is_staff=True باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('ابرکاربر باید is_superuser=True باشد.')

        return self.create_user(username, password, **extra_fields)

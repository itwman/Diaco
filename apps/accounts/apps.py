"""
Diaco MES - Accounts Application Config
=========================================
مدیریت کاربران، احراز هویت و نقش‌ها.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'مدیریت کاربران'
    verbose_name_plural = 'مدیریت کاربران'

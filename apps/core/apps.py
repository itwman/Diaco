"""
Diaco MES - Core Application Config
=====================================
هسته مشترک سیستم: ماشین‌آلات، شیفت، لاگ، اعلان.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'هسته سیستم'
    verbose_name_plural = 'هسته سیستم'

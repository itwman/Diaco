"""
Diaco MES - Winding App Config (بوبین‌پیچی)
"""
from django.apps import AppConfig


class WindingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.winding'
    verbose_name = 'بوبین‌پیچی'

    def ready(self):
        import apps.winding.signals  # noqa: F401

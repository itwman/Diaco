"""
Diaco MES - Inventory Application Config
==========================================
مدیریت انبار مواد اولیه: الیاف، رنگ، مواد شیمیایی.
"""
from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = 'انبار مواد اولیه'
    verbose_name_plural = 'انبار مواد اولیه'

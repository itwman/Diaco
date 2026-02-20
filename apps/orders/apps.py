"""
Diaco MES - Orders Application Config
=======================================
مدیریت سفارشات، مشتریان و شید رنگی.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
    verbose_name = 'سفارشات'
    verbose_name_plural = 'سفارشات'

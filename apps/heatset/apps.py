"""
Diaco MES - HeatSet App Config (هیت‌ست)
"""
from django.apps import AppConfig


class HeatsetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.heatset'
    verbose_name = 'هیت‌ست'

    def ready(self):
        import apps.heatset.signals  # noqa: F401

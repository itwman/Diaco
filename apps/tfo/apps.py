"""
Diaco MES - TFO App Config (دولاتابی)
"""
from django.apps import AppConfig


class TfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tfo'
    verbose_name = 'دولاتابی TFO'

    def ready(self):
        import apps.tfo.signals  # noqa: F401

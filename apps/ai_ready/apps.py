from django.apps import AppConfig


class AiReadyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ai_ready'
    verbose_name = 'آماده‌سازی AI'

    def ready(self):
        import apps.ai_ready.signals  # noqa

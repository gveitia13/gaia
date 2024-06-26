from django.apps import AppConfig


class AppMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_main'
    verbose_name = 'Principal'
    verbose_name_plural = 'Principales'

    def ready(self):
        import app_main.signals

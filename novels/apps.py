from django.apps import AppConfig


class NovelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'novels'

# novels/apps.py
from django.apps import AppConfig

class NovelsConfig(AppConfig):
    name = 'novels'

    def ready(self):
        import novels.signals

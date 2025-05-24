from django.apps import AppConfig

class CursosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cursos'
from django.apps import AppConfig

class CursosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cursos'

    def ready(self):
        import apps.cursos.signals

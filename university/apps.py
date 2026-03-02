from django.apps import AppConfig

class AcademicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'university'

    def ready(self):
        import university.signals  # enregistre les signaux
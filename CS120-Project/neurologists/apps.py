from django.apps import AppConfig

class NeurologistsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'neurologists'

    def ready(self):
        import neurologists.signals  # noqa 
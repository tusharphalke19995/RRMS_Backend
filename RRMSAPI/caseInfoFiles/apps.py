from django.apps import AppConfig


class CaseinfofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'caseInfoFiles'

    def ready(self):
        import caseInfoFiles.signals
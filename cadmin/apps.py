from django.apps import AppConfig


class CadminConfig(AppConfig):
    name = 'cadmin'

    def ready(self):
        import cadmin.signals

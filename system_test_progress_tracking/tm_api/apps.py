from django.apps import AppConfig


class TmApiConfig(AppConfig):
    name = 'tm_api'

    def ready(self):
        import tm_api.signals

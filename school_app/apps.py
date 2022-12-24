from django.apps import AppConfig


class SchoolAppConfig(AppConfig):
    name = 'school_app'
    def ready(self):
        from.scheduler import start
        start()

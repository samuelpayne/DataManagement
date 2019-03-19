"""Project DataMan

Connects this for Django."""

from django.apps import AppConfig

class RecordsConfig(AppConfig):
    name = 'Records'

    def ready(self):
        from Records import views
        views.start_job()

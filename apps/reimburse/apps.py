from django.apps import AppConfig


class ReimburseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reimburse'
    
    def ready(self):
        from . import signals


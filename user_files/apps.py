from django.apps import AppConfig


class UserFilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_files'

    def ready(self):
        import rosstat.celery
        from rosstat.celery import app

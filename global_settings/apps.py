from django.apps import AppConfig


class GlobalSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'global_settings'

    def ready(self):
        from django.db.models.signals import post_migrate
        from global_settings.models import GlobalSettings
        import global_settings.signals

        def configure_yandex_storage(sender, **kwargs):
            from rosstat.backend_storages import YandexStorage
            try:
                settings = GlobalSettings.objects.get(id=1)
                YandexStorage.querystring_expire = settings.url_lifetime_seconds
            except GlobalSettings.DoesNotExist:
                pass

        post_migrate.connect(configure_yandex_storage, sender=self)

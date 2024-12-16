from django.db.models.signals import post_save
from django.dispatch import receiver
from global_settings.models import GlobalSettings
from rosstat.backend_storages import YandexStorage


@receiver(post_save, sender=GlobalSettings)
def set_settings(sender, instance: GlobalSettings, created, **kwargs):
    settings = GlobalSettings.objects.get(id=1)
    YandexStorage.querystring_expire = settings.url_lifetime_seconds

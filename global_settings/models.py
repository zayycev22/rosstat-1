from django.db import models

from global_settings.consts import FileExtensionConsts


# Create your models here.
class GlobalSettings(models.Model):
    file_size = models.IntegerField(default=5, verbose_name="Максимальный размер файла в мегабайтах")
    file_lifetime_seconds = models.IntegerField(default=2678400, verbose_name="Время жизни файла в секундах")
    url_lifetime_seconds = models.IntegerField(default=3600, verbose_name="Время жизни ссылки в секундах")

    class Meta:
        verbose_name = "Глобальные настройки"
        verbose_name_plural = "Глобальные настройки"
        db_table = "global_settings"


class FileExtension(models.Model):
    extension = models.CharField(max_length=4, verbose_name="Расширение файла", choices=FileExtensionConsts.extensions,
                                 unique=True)

    def __str__(self):
        return self.extension

    class Meta:
        verbose_name = "Расширение файла"
        verbose_name_plural = "Расширения файлов"
        db_table = "file_extension"

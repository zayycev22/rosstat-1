from django.db import models

from auth_user.models import ExUser


class UserFile(models.Model):
    user = models.ForeignKey(ExUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    file = models.FileField(verbose_name="Файл")
    filename = models.CharField(max_length=128)
    created_exp = models.DateTimeField(verbose_name="Дата удаления")

    def __str__(self):
        return self.file.name

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete()

    class Meta:
        verbose_name = "Файл пользователя"
        verbose_name_plural = "Файлы пользователя"
        db_table = "user_file"

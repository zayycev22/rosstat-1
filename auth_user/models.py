from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from auth_user.manager import EmailUserManager


# Create your models here.
class ExUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Почта", unique=True)
    name = models.CharField(verbose_name="Имя", max_length=50, null=True, blank=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="",
    )

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    objects = EmailUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

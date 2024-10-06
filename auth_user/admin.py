from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token

from auth_user.forms import EmailUserCreationForm, EmailChangeForm
from auth_user.models import ExUser


class TokenInline(admin.StackedInline):
    model = Token
    can_delete = False
    max_num = 1


class ExUserAdmin(UserAdmin):
    list_display = ("email",)
    inlines = [TokenInline]
    fieldsets = (
        (None,
         {'fields': (
             'email', 'password', 'name', 'surname',
             'is_superuser')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email", "name", "surname",
                    "password1", "password2", "is_superuser", 'is_staff'),
            },
        ),
    )
    list_filter = ("is_superuser",)
    search_fields = ("email", "name")
    ordering = ("email",)
    add_form = EmailUserCreationForm
    form = EmailChangeForm


admin.site.register(ExUser, ExUserAdmin)
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from auth_user.models import ExUser


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("email",)
        field_classes = {"email": forms.EmailField}


class EmailChangeForm(UserChangeForm):
    class Meta:
        model = ExUser
        fields = "__all__"
        field_classes = {"email": forms.EmailField}

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Электронная почта")
    password2 = None
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ("first_name", "username", "email")

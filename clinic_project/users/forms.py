from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # Убрано поле 'role'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    birth_year = forms.IntegerField(
        label="Год рождения",
        min_value=1900,
        max_value=2100
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "birth_year", "password1", "password2")
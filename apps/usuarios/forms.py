from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django_select2.forms import Select2MultipleWidget

from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label="Correo electrónico", max_length=50,
    widget=forms.TextInput(attrs={
         'id': 'usernameInput',
         'placeholder': 'Correo electrónico',
         'class': 'form-control'
    }))
    password = forms.CharField(label="Contraseña", max_length=50,
    widget=forms.TextInput(attrs={
        'type': 'password',
        'id': 'passwordInput',
        'placeholder': 'Contraseña',
         'class': 'form-control'
    }))

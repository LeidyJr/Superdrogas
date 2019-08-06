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

class CrearUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['first_name'].label = "Nombres*"
        self.fields['last_name'].label = "Apellidos*"
        self.fields['email'].label = "Dirección de correo electrónico*"
        self.fields['password1'].label = "Contraseña nueva*"
        self.fields['password2'].label = "Confirmar contraseña nueva*"

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',)

    def clean_first_name(self):
        nombres = self.cleaned_data['first_name']
        nombres = nombres.strip().title()
        return nombres

    def clean_last_name(self):
        apellidos = self.cleaned_data['last_name']
        apellidos = apellidos.strip().title()
        return apellidos

    def clean(self):
        form_data = self.cleaned_data
        try:
            usuario_encontrado = Usuario.objects.get(email=form_data["email"])
            usuario_actual = self.instance
            if usuario_actual:
                if usuario_actual != usuario_encontrado:
                    self._errors["email"] = ["El correo electrónico del usuario ya existe"]
            else:
                self._errors["email"] = ["El correo electrónico del usuario ya existe"]
        except Usuario.DoesNotExist:
            pass

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['groups'].label = "Grupo al que pertenece el trabajador"
        self.fields['groups'].help_text = "El trabajador tendrá todos los permisos asignados al grupo"

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', "groups",)
        widgets = {
            "groups": Select2MultipleWidget,
        }

    def clean(self):
        form_data = self.cleaned_data
        try:
            usuario_encontrado = Usuario.objects.get(email=form_data["email"])
            usuario_actual = self.instance
            if usuario_actual:
                if usuario_actual != usuario_encontrado:
                    self._errors["email"] = ["El correo electrónico del usuario ya existe"]
            else:
                self._errors["email"] = ["El correo electrónico del usuario ya existe"]
        except Usuario.DoesNotExist:
            pass

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ("tipo_documento", "numero_documento", "fecha_nacimiento", "genero", "celular", "imagen",)

    def __init__(self, *args, **kwargs):
        super(TrabajadorForm, self).__init__(*args, **kwargs)
        self.fields["fecha_nacimiento"].widget.attrs.update({
            'class': 'fecha2 readonly'
        })

class ClienteForm(forms.ModelForm):
    terminos_condiciones = forms.BooleanField()
    class Meta:
        model = Cliente
        fields = ("genero",)

    def __init__(self, *args, **kwargs):
        from django.utils.safestring import mark_safe
        from django.conf import settings
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['terminos_condiciones'].label = mark_safe(("He leído y estoy de acuerdo con los Términos, condiciones, políticas y tratamiento de datos personales*"))

    def clean_message(self):
        terminos_condiciones = self.cleaned_data['terminos_condiciones']
        if terminos_condiciones == False:
            raise ValidationError('Los términos, condiciones, políticas y tratamiento de datos personales deben ser aceptados')
        return terminos_condiciones

class RestablecerContrasenaForm(forms.Form):
    password1 = forms.CharField(
        label = 'Contraseña nueva', max_length = 50,
        widget = forms.TextInput(attrs = {
        'type': 'password',
        'placeholder': 'Contraseña',
        'data-parsley-contrasena': '',
        'class': 'form-control'
    }))

    password2 = forms.CharField(label = 'Confirmar contraseña nueva', max_length = 50,
        widget = forms.TextInput(attrs = {
        'type': 'password',
        'placeholder': 'Confirmar contraseña',
        'data-parsley-confirmacion': 'id_password1',
        'class': 'form-control'
    }))

    def clean(self):
        form_data = self.cleaned_data
        if form_data["password1"] != form_data["password2"]:
            self._errors["password2"] = ["Las contraseñas no coinciden"]
        return form_data
from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from .models import *

class RegistrarEmpresaForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        super(RegistrarEmpresaForm, self).__init__(*args, **kwargs)
        self.fields['schema_name'].label = "Página web la cual estará asignada a su empresa"
        self.fields['schema_name'].help_text = ("Esta será su página web: midireccion%s")%(settings.DOMAIN)

    class Meta:
        model = Empresa
        fields = ("nombre", "schema_name",)

class ModificarEmpresaForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Empresa
        fields = ("nombre",)
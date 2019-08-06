from django import forms

from .models import Categoria

class RegistrarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nombre", "descripcion",)

    def __init__(self, *args, **kwargs):
        super(RegistrarCategoriaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 5
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none'
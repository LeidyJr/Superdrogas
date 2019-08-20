from django import forms

from .models import Medicamento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ("nombre", "precio", "categoria", "imagen", "descripcion", "activo", "cantidad", "unidad_medida", )

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 5
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none'
from django import forms

from .models import Lote

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ("fecha_fabricacion", "fecha_vencimiento", "producto", "cantidad", "activo",)

    def __init__(self, *args, **kwargs):
        super(LoteForm, self).__init__(*args, **kwargs)
        self.fields["fecha_fabricacion"].widget.attrs.update({
            'class': 'fecha readonly'
        })
        self.fields["fecha_vencimiento"].widget.attrs.update({
            'class': 'fecha readonly'
        })

    def clean_fecha(self):
        fecha_fabricacion = self.cleaned_data['fecha_fabricacion']
        fecha_vencimiento = self.cleaned_data['fecha_vencimiento']
        if fecha_fabricacion > fecha_vencimiento:
            raise forms.ValidationError('La fecha de vencimiento no puede ser inferior a la fecha de fabricación.')
        return fecha_vencimiento
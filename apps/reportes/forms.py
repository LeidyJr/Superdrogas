from django import forms
from django.core.exceptions import ValidationError

from datetime import datetime

class PeriodoTiempoForm(forms.Form):
    fecha_inicio = forms.DateField(label="Fecha de inicio")
    fecha_fin = forms.DateField(label="Fecha de fin")

    def __init__(self, *args, **kwargs):
        super(PeriodoTiempoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'fecha readonly'
            })

    def clean(self):
        inicio = self.cleaned_data['fecha_inicio']
        fin = self.cleaned_data['fecha_fin']
        if inicio >= fin:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser menor a la fecha de inicio')
        return  self.cleaned_data

class FechaForm(forms.Form):
    fecha = forms.DateField(label="Fecha de análisis")
    def __init__(self, *args, **kwargs):
        super(FechaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'fecha readonly'
            })


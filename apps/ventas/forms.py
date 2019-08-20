from django import forms
from django.core.exceptions import ValidationError

from apps.usuarios.models import Usuario
from .models import Venta, VentaProducto

class VentaProductoForm(forms.ModelForm):
    class Meta:
        model = VentaProducto
        fields = ("producto", "cantidad", "precio", "descuento",)

class SeleccionarClienteForm(forms.Form):

    cliente = forms.ModelChoiceField(queryset = Usuario.objects.filter(rol="Cliente"))

    def clean_cliente(self):
        data = self.cleaned_data.get('cliente')
        return data
from rest_framework import serializers

from .models import Medicamento

class MedicamentoSerializador(serializers.ModelSerializer):
    imagen = serializers.CharField(source='obtener_imagen', read_only=True)

    class Meta:
        model = Medicamento
        fields = ('id', 'nombre', 'precio', 'descripcion', 'imagen', )

from .models import Categoria
from rest_framework import serializers

from apps.medicamentos.serializers import MedicamentoSerializador
from apps.medicamentos.models import Medicamento

class CategoriaSerializador(serializers.ModelSerializer):
    medicamentos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ('nombre', 'descripcion', 'cantidad_productos', 'medicamentos',)

    def get_productos(self, categoria):
        qs = Medicamento.objects.filter(categoria=categoria, activo=True)
        serializer = MedicamentoSerializador(many=True, read_only=True, instance=qs)
        return serializer.data
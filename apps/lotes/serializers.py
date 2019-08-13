from rest_framework import serializers

from .models import Lote

class LoteSerializador(serializers.ModelSerializer):

    class Meta:
        model = Lote
        fields = ('id', 'fecha_fabricacion', 'fecha_vencimiento', 'cantidad', 'producto', 'activo', )

from django.db import models

from simple_history.models import HistoricalRecords

from apps.empresas.models import Empresa

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="nombre de la categoría de productos*", help_text="Ejemplo: Vitaminas")
    descripcion = models.TextField(blank=True, verbose_name="descripción (opcional)")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    historial = HistoricalRecords()

    class Meta:
        ordering = ['nombre']
        permissions = (
            ("gestionar_categorias", "Gestión de categorias"),
        )

    def cantidad_productos(self):
        from apps.medicamentos.models import Medicamento
        return Medicamento.objects.filter(categoria=self).count()

    def __str__(self):
        return self.nombre
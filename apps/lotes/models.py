from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_history.models import HistoricalRecords

from apps.medicamentos.models import Medicamento

class Lote(models.Model):
    fecha_fabricacion = models.DateField()
    fecha_vencimiento = models.DateField()
    producto = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name="producto del lote*", related_name="productos")
    cantidad = models.PositiveIntegerField(verbose_name="cantidad actual*")
    activo = models.BooleanField(default=True, verbose_name="¿El lote está activo actualmente?")

    historial = HistoricalRecords()
    
    class Meta:
        ordering = ["producto__nombre"]
        permissions = (
            ("gestionar_lotes", "Gestión de lotes"),
        )

    def __str__(self):
        return ("%s(%s)(%s)"%(self.producto.nombre, self.fecha_vencimiento, self.cantidad))


    @staticmethod
    def obtener_listado():
        return Lote.objects.all()

    @staticmethod
    def existe_medicamento_activo():
        return Lote.obtener_activos().exists()

    @staticmethod
    def obtener_activos():
        return Lote.objects.filter(activo=True)

    def cambiar_estado(self):
        self.activo = not(self.activo)
        self.save()

    def obtener_estado(self):
        if self.activo:
            return "Activo"
        return "Inactivo"

    def obtener_nombre_producto(self):
        return self.producto.nombre
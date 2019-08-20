from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from apps.medicamentos.models import Medicamento
from apps.usuarios.models import Usuario

class Venta(models.Model):
    cliente = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE, related_name="cliente")
    trabajador = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE, related_name="trabajador")
    fecha = models.DateTimeField()
    subtotal = models.PositiveIntegerField(default=0)
    iva = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    terminada = models.DateTimeField(null=True)
    cancelado = models.BooleanField(default=False)

    historial = HistoricalRecords()

    class Meta:
        ordering = ("fecha",)
        permissions = (
            ("gestionar_ventas", "Gestión de ventas"),
        )

    def save(self, *args, **kwargs):
        
        if not self.id:
            self.fecha = timezone.now()
        return super(Venta, self).save(*args, **kwargs)



    def cancelar(self, motivo):
        VentaCancelacion.objects.create(venta=self, motivo=motivo)
        self.cancelado = True
        self.terminada = None
        self.save()


    @staticmethod
    def obtener_venta_activa(request, cliente, trabajador):
        if "venta_activa" in request.session:
            return Venta.objects.get(id=request.session["venta_activa"])
        else:
            venta = Venta.objects.create(cliente=cliente, trabajador=trabajador)
            request.session["venta_activa"] = venta.id
            return venta

    @staticmethod
    def obtener_venta(request):
        if "venta_activa" in request.session:
            return Venta.objects.get(id=request.session["venta_activa"])
        return None

    def cerrar_venta(self):
        if self.terminada == None:
            return
        
        venta_productos = self.productos_comprados.all()
        for venta_producto in venta_productos:
            venta_producto.cerrar_venta()

    def eliminar_venta(self):
        if self.terminada == None:
            return
        
        venta_productos = self.productos_comprados.all()
        for venta_producto in venta_productos:
            venta_producto.eliminar()

class VentaCancelacion(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name="cancelacion")
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()

    historial = HistoricalRecords()

class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="productos_comprados")
    producto = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name="producto")
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()
    descuento = models.PositiveIntegerField(default=0)

    historial = HistoricalRecords()

    def __str__(self):
        return ("%s (%s)"%(self.producto.nombre, self.cantidad))

    def cerrar_venta(self):
        print(self.producto.cantidad)
        print(self.cantidad)
        self.producto.cantidad -= self.cantidad
        print(self.cantidad)

    def eliminar(self):
        self.producto.cantidad -= self.cantidad

    def calcular_total(self):
        return (self.precio * self.cantidad) - self.descuento


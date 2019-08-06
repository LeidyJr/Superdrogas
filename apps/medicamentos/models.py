from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.usuarios.models import Usuario
from apps.categorias.models import Categoria

def crear_ruta_medicamento(instance, filename):
    print("***********",instance, filename)
    return "empresa-%s/productos/%s"%(instance.categoria.empresa.id, filename.encode('ascii','ignore'))

class Medicamento(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="nombre del producto*", unique=True)
    unidad_medida = models.CharField(max_length=50, verbose_name="unidad de medida*")
    precio = models.PositiveIntegerField(verbose_name="precio de venta*")
    cantidad = models.PositiveIntegerField(verbose_name="cantidad actual*")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="categoría del producto*", related_name="productos")
    descripcion = models.TextField(blank=True, verbose_name="descripción")
    imagen = models.ImageField(upload_to="crear_ruta_medicamento", blank=True, verbose_name="imagen del producto")
    activo = models.BooleanField(default=True, verbose_name="¿El producto está activo actualmente?")

    class Meta:
        ordering = ["nombre"]
        permissions = (
            ("gestionar_productos", "Gestión de productos"),
        )

    def __str__(self):
        return ("%s"%(self.nombre))

    def obtener_imagen(self):
        from django.conf import settings
        if self.imagen in [None, ""]:
            return ("%s%s")%(settings.MEDIA_URL, self.categoria.empresa.logo)
        return ("%s")%(self.imagen.url)

    @staticmethod
    def obtener_listado():
        return Medicamento.objects.all()

    @staticmethod
    def existe_medicamento_activo():
        return Medicamento.obtener_activos().exists()

    @staticmethod
    def obtener_activos():
        return Medicamento.objects.filter(activo=True)

    def cambiar_estado(self):
        self.activo = not(self.activo)
        self.save()

    def obtener_estado(self):
        if self.activo:
            return "Activo"
        return "Inactivo"

@receiver(post_save, sender=Medicamento, dispatch_uid="minificar_imagen_medicamento")
def comprimir_imagen(sender, **kwargs):
    from apps.core.utils import comprimir_imagen
    if kwargs["instance"].imagen:
        comprimir_imagen(kwargs["instance"].imagen)

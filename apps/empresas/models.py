from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django_tenants.models import TenantMixin, DomainMixin

def crear_ruta_logo(instance, filename):
    return "empresas/logo/%s"%(filename.encode('ascii','ignore'))

class Empresa(TenantMixin):
    nombre = models.CharField(max_length=100, verbose_name="nombre de la empresa")
    sobre_nosotros = models.TextField(verbose_name="sobre nosotros (descripción de su negocio)*")
    eslogan = models.CharField(max_length=100, verbose_name="eslogan de su negocio*")
    email = models.EmailField(verbose_name="correo electrónico del negocio*")
    direccion = models.CharField(max_length=100, verbose_name="dirección del negocio*")
    telefono = models.CharField(max_length=100, verbose_name="teléfono del negocio*")
    logo = models.ImageField(upload_to=crear_ruta_logo, verbose_name="logo del negocio", blank=True)
    creado = models.DateField(auto_now_add=True)
    auto_create_schema = True
    # default true, schema will be automatically created and synced when it is saved

    def __str__(self):
        return self.nombre

    class Meta:
        permissions = (
            ("gestionar_empresas", "Gestión de empresas"),
        )

class Dominio(DomainMixin):
    pass
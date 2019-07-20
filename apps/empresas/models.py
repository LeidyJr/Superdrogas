from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    nombre = models.CharField(max_length=100, verbose_name="nombre de la empresa")
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
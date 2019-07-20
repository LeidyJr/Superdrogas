from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse

class Usuario(AbstractUser):
    ROLES = (
        ("Cliente", "Cliente"),
        ("Trabajador", "Trabajador"),
    )
    rol = models.CharField(max_length=100, choices=ROLES)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = (
            ("gestionar_usuarios", "Gestión de usuarios"),
        )

    def save(self, *args, **kwargs):
        self.username = self.email
        super(Usuario, self).save(*args, **kwargs)



class Trabajador(models.Model):
    GENEROS = (
        ("Mujer", "Mujer"),
        ("Hombre", "Hombre"),
        ("Otro", "Otro"),
    )
    TIPOS_DOCUMENTOS = (
        ("Cédula de ciudadanía", "Cédula de ciudadanía"),
        ("Cédula de extranjería", "Cédula de extranjería"),
        ("Tarjeta de identidad", "Tarjeta de identidad"),
        ("Pasaporte", "Pasaporte"),
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="datos_trabajador")
    tipo_documento = models.CharField(max_length=50, choices=TIPOS_DOCUMENTOS, verbose_name="tipo de documento de identidad*")
    numero_documento = models.CharField(max_length=50, verbose_name="número de documento de identidad*")
    fecha_nacimiento = models.DateField(verbose_name="fecha de nacimiento*")
    genero = models.CharField(max_length=20, choices=GENEROS, verbose_name="género*")
    celular = models.CharField(max_length=25, verbose_name="número de celular*")

class Cliente(models.Model):
    GENEROS = (
        ("Mujer", "Mujer"),
        ("Hombre", "Hombre"),
        ("Otro", "Otro"),
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="datos_cliente")
    genero = models.CharField(max_length=20, choices=GENEROS, verbose_name="género", blank=True)
    acepto_terminos_condiciones = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import AbstractUser, Group

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse

class Usuario(AbstractUser):
    ROLES = (
        ("Cliente", "Cliente"),
        ("Trabajador", "Trabajador"),
    )
    rol = models.CharField(max_length=100, choices=ROLES)

    def get_absolute_url(self):
        return reverse("usuarios:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = (
            ("gestionar_usuarios", "Gestión de usuarios"),
        )

    # def obtener_pagina_inicio(self):
    #     if self.rol == "Trabajador":
    #         return "ventas:inicio_empresa"
    #     return "ventas:inicio"

    def obtener_datos_rol(self):
        if self.rol == "Trabajador":
            print(self.datos_trabajador)
            return self.datos_trabajador
        return self.datos_cliente

    def save(self, *args, **kwargs):
        self.username = self.email
        super(Usuario, self).save(*args, **kwargs)

    @staticmethod
    def crear_grupos():
        total_grupos = Group.objects.all().count()
        if total_grupos == 0:
            Group.objects.create(name="Trabajador")
            Group.objects.create(name="Cliente")

    @staticmethod
    def crear_usuario_inicial():
        total_usuarios = Usuario.objects.all().count()
        if total_usuarios == 0:
            password = "administrador"
            usuario = Usuario.objects.create_user('admin', 'admin@gmail.com', password)
            usuario.set_password(password)
            usuario.first_name = 'Administrador'
            usuario.is_superuser = True
            usuario.is_staff = True
            usuario.rol = "Trabajador"
            usuario.save()

            grupo = Group.objects.get(name="Trabajador")
            grupo.user_set.add(usuario)

            Trabajador.objects.create(usuario=usuario, tipo_documento="Cédula de ciudadanía", numero_documento="123456789",
                fecha_nacimiento="2019-01-01", genero="Mujer", celular="321654987")



def crear_ruta_trabajador(instance, filename):
    return "empresas/empleados/%s"%(filename.encode('ascii','ignore'))

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
    imagen = models.ImageField(upload_to=crear_ruta_trabajador, blank=True, null=True, verbose_name="imagen del trabajador")

    def obtener_imagen(self):
        from django.conf import settings
        if self.imagen in [None, ""]:
            return ("%s%s")%(settings.MEDIA_URL, self.imagen)
        return ("%s")%(self.imagen.url)

@receiver(post_save, sender=Trabajador, dispatch_uid="minificar_imagen_trabajador")
def comprimir_imagen(sender, **kwargs):
    from apps.core.utils import comprimir_imagen
    if kwargs["instance"].imagen:
        comprimir_imagen(kwargs["instance"].imagen)

class Cliente(models.Model):
    GENEROS = (
        ("Mujer", "Mujer"),
        ("Hombre", "Hombre"),
        ("Otro", "Otro"),
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="datos_cliente")
    genero = models.CharField(max_length=20, choices=GENEROS, verbose_name="género", blank=True)
    acepto_terminos_condiciones = models.DateTimeField(auto_now_add=True)

from django.db import models

from apps.usuarios.models import Usuario

class LogApp(models.Model):
    PETICIONES = (
        ("GET", "GET"),
        ("POST", "POST"),
    )
    accion = models.TextField()
    usuario = models.CharField(max_length=150)
    grupo_usuario = models.CharField(max_length=150)
    fecha_log = models.DateField('timestamp', auto_now=True)
    hora_log = models.TimeField('timestamp', auto_now=True)
    ip_cliente = models.CharField(max_length=50)
    peticion = models.CharField(max_length=50, choices=PETICIONES)

    def log(self, request, msg, peticion):
        self.accion = msg
        self.peticion = peticion
        self.ip_cliente = obtener_direccion_ip(request)
        self.usuario, self.grupo_usuario = obtener_usuario_y_grupo(request)
        self.save()

    def crear_log(request, msg):
        log = LogApp()
        log.accion = msg
        log.peticion = request.method
        log.ip_cliente = obtener_direccion_ip(request)
        log.usuario, log.grupo_usuario = obtener_usuario_y_grupo(request)
        log.save()

def obtener_usuario_y_grupo(request):
    usuario = request.user
    if usuario.is_authenticated:
        try:
            grupo = usuario.groups.all()[0]
            return usuario.username, grupo
        except IndexError:
            return usuario.username, "No especificado"
    return "", "No especificado"

def obtener_direccion_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LogActualizacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    duracion = models.DurationField()
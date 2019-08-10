from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "usuarios"
urlpatterns = [
	url(regex=r"^iniciar-sesion$", view=views.Login.as_view(), name='login'),
	url(regex=r"^cerrar-sesion$", view=views.Logout, name='logout'),
	url(regex=r"^registro-cliente$", view=views.RegistrarCliente, name='regisrar_cliente'),
	url(regex=r"^registrar-trabajador$", view=views.RegistrarTrabajador, name='registrar_trabajador'),
	url(regex=r"^modificar-trabajador/(\d+)$", view=views.RegistrarTrabajador, name='modificar_trabajador'),
	url(regex=r"^listado$", view=views.ListadoUsuarios.as_view(), name='listado'),
    url(regex=r'^desactivar/(?P<id_usuario>\d+)$', view=views.DesactivarUsuario, name="desactivar"),
    url(regex=r'^activar/(?P<id_usuario>\d+)$', view=views.ActivarUsuario, name="activar"),
    url(regex=r'^asignacion-administrador/(?P<id_usuario>\d+)$', view=views.AsignacionAdministrador, name="asignacion_administrador"),
	
    url(regex=r"^todos/$", view=views.UsuarioListado.as_view(), name='todos'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "usuarios"
urlpatterns = [
	path("iniciar-sesion", view=views.Login.as_view(), name='login'),
	path("cerrar-sesion", view=views.Logout, name='logout'),
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "usuarios"
urlpatterns = [
	url(regex=r"^iniciar-sesion$", view=views.Login.as_view(), name='login'),
	url(regex=r"^cerrar-sesion$", view=views.Logout, name='logout'),
	
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "grupos"
urlpatterns = [
	url(regex=r"^registrar$", view=views.RegistrarGrupo.as_view(), name="registrar"),
    url(regex=r"^modificar/(?P<pk>[\w-]+)$", view=views.ModificarGrupo.as_view(), name="modificar"),
    url(regex=r"^listado$", view=views.ListadoGrupo.as_view(), name="listado"),
]

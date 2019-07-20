from django.conf.urls import url
from django.urls import path

from . import views

app_name = "empresas"
urlpatterns = [
    path("registrar", view=views.RegistrarEmpresa.as_view(), name="registrar"),
    path("modificar/<int:pk>", view=views.ModificarEmpresa.as_view(), name="modificar"),
    path("listado", view=views.ListadoEmpresa.as_view(), name="listado"),
]
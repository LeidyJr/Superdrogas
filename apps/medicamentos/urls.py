from django.urls import path

from .views import *

app_name = 'medicamentos'

urlpatterns = [
    path("registrar", view=Registrar.as_view(), name='registrar'),
    path("listado", view=Listado.as_view(), name="listado"),
    path("modificar/<int:pk>", view=Modificar.as_view(), name='modificar'),
	path("consultar/<int:pk>", view=Consultar.as_view(), name='consultar'),    
]
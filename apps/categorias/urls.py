from django.conf.urls import url

from . import views

app_name = "categorias"
urlpatterns = [
    url(regex=r"^registrar$", view=views.RegistrarCategoria.as_view(), name="registrar"),
    url(regex=r"^modificar/(?P<pk>[\w-]+)$", view=views.ModificarCategoria.as_view(), name="modificar"),
    url(regex=r"^listado$", view=views.ListadoCategoria.as_view(), name="listado"),
    url(regex=r"^inicio$", view=views.Inicio.as_view(), name="inicio"),
    url(regex=r"^todos$", view=views.APICategoria.as_view(), name='todos'),
]
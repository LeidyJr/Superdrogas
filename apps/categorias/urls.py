from django.conf.urls import url

from . import views

app_name = "categorias"
urlpatterns = [
    url(regex=r"^registrar$", view=views.RegistrarCategoria.as_view(), name="registrar"),
    url(regex=r"^modificar/(?P<pk>[\w-]+)$", view=views.ModificarCategoria.as_view(), name="modificar"),
    url(regex=r"^listado$", view=views.ListadoCategoria.as_view(), name="listado"),
    url(regex=r"^inicio-ventas$", view=views.InicioVentas.as_view(), name="inicio_ventas"),
    url(regex=r"^inicio-compras$", view=views.InicioCompras.as_view(), name="inicio_compras"),
    url(regex=r"^todos$", view=views.APICategoria.as_view(), name='todos'),
]
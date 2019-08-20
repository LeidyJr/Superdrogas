from django.conf.urls import url

from .views import *

app_name = "ventas"
urlpatterns = [ # Administradores
	url(regex=r"^agregar/(?P<id_producto>[\w-]+)$", view=nueva_venta, name="agregar"),
	url(regex=r"^eliminar/(?P<id_producto>[\w-]+)$", view=eliminar_producto_carrito, name="eliminar"),
	url(regex=r"^finalizar-venta$", view=finalizar_venta, name="finalizar_venta"),
]
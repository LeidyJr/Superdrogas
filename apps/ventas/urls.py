from django.conf.urls import url

from .views import *

app_name = "ventas"
urlpatterns = [ # Administradores
	url(regex=r"^agregar/(?P<id_producto>[\w-]+)$", view=nueva_compra, name="agregar"),
	url(regex=r"^eliminar/(?P<id_producto>[\w-]+)$", view=eliminar_producto_carrito_compra, name="eliminar"),
	url(regex=r"^finalizar-venta$", view=finalizar_compra, name="finalizar_venta"),
]
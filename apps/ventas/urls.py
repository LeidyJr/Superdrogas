from django.conf.urls import url

from .views import *

app_name = "ventas"
urlpatterns = [ 
	url(regex=r"^agregar/(?P<id_producto>[\w-]+)$", view=nueva_venta, name="agregar"),
	url(regex=r"^eliminar/(?P<id_producto>[\w-]+)$", view=eliminar_producto_carrito, name="eliminar"),
	url(regex=r"^finalizar-venta$", view=finalizar_venta, name="finalizar_venta"),
	url(regex=r"^agregar-compra/(?P<id_producto>[\w-]+)$", view=nueva_compra, name="agregar_compra"),
	url(regex=r"^eliminar-compra/(?P<id_producto>[\w-]+)$", view=eliminar_producto_carrito_compra, name="eliminar_compra"),
	url(regex=r"^finalizar-compra$", view=finalizar_compra, name="finalizar_compra"),
	url(r'^factura/(?P<pk>\d+)/$', view=ver_factura, name='factura'),
]
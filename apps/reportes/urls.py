from django.conf.urls import url

from . import views

app_name = "reportes"
urlpatterns = [
	url(regex=r"^detalles-ventas-diarias$", view=views.DetallesVentasDiarias, name="detalles_ventas_diarias"),
	url(regex=r"^ventas-por-productos$", view=views.VentasPorProductos, name="ventas_por_productos"),
	url(regex=r"^ventas-por-categoria$", view=views.VentasPorCategoria, name="ventas_por_categoria"),
	url(regex=r"^ventas-por-cliente$", view=views.VentasPorCliente, name="ventas_por_cliente"),
	url(regex=r"^ventas-por-vendedor$", view=views.VentasPorVendedor, name="ventas_por_vendedor"),
	url(regex=r"^ventas-diarias$", view=views.VentasDiariasP, name="ventas_diarias"),
	url(regex=r"^disponibilidad-productos$", view=views.DisponibilidadProductos, name="disponibilidad_productos"),
 ]
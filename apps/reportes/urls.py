from django.conf.urls import url

from . import views

app_name = "reportes"
urlpatterns = [
	url(regex=r"^detalles-ventas-diarias$", view=views.DetallesVentasDiarias, name="detalles_ventas_diarias"),
	url(regex=r"^ventas-por-productos$", view=views.VentasPorProductos, name="ventas_por_productos"),
	 url(regex=r"^ventas-diarias$", view=views.VentasDiariasP, name="ventas_diarias"),
 ]
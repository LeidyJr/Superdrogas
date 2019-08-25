from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import *
from .generador_reportes import *
from apps.core.utils import agregar_por

@login_required
def DetallesVentasDiarias(request):
    from django.db.models import Sum
    hoy = timezone.localdate().strftime('%Y-%m-%d')
    fecha = request.GET.get("fecha", hoy)
    form = FechaForm(initial={"fecha": fecha})
    if "fecha" in request.GET:
        form = FechaForm(request.GET, initial={"fecha": fecha})
        if form.is_valid():
            ventas = DetallesVentas(fecha)
        else:
            for campo, error in form.errors.items():
                messages.error(request, error[0])
            ventas = DetallesVentas(fecha)
    else:
        ventas = DetallesVentas(fecha)
    
    total_ventas = agregar_por(ventas, Sum, 'total')

    return render(request, "reportes/registro_ventas.html", {
        "form": form,
        "ventas": ventas,
        "fecha": fecha,
        'total_ventas': total_ventas,
    })

@permission_required('reportes.gestionar_reportes')
def VentasPorProductos(request):
    hoy = timezone.localdate().strftime('%Y-%m-%d')
    fecha = request.GET.get("fecha", hoy)
    form = FechaForm(initial={"fecha": fecha})
    if "fecha" in request.GET:
        form = FechaForm(request.GET, initial={"fecha": fecha})
        if form.is_valid():
            productos = DetallesVentasProductos(fecha)
        else:
            for campo, error in form.errors.items():
                messages.error(request, error[0])
            productos = DetallesVentasProductos(fecha)
    else:
        productos = DetallesVentasProductos(fecha)
    
    return render(request, "reportes/ventas_por_productos.html", {
        "form": form,
        "productos": productos,
        "fecha": fecha,
    })

@login_required
@permission_required('reportes.gestionar_reportes')
def VentasDiariasP(request):
    fecha_inicio, fecha_fin = request.GET.get("fecha_inicio", ""), request.GET.get("fecha_fin", "")
    form = PeriodoTiempoForm()
    if "fecha_inicio" in request.GET:
        form = PeriodoTiempoForm(request.GET)
        if form.is_valid():
            datos = VentasDiarias(fecha_inicio, fecha_fin)
        else:
            for campo, error in form.errors.items():
                messages.error(request, error[0])
            datos = VentasDiarias()
    else:
        datos = VentasDiarias()
    
    return render(request, "reportes/ventas_diarias.html", {
        "form": form,
        "datos": list(datos),
        "titulo": "Dinero ($)",
    })

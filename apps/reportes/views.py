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
            datos = DetallesVentasProductos(fecha)
        else:
            for campo, error in form.errors.items():
                messages.error(request, error[0])
            datos = DetallesVentasProductos(fecha)
    else:
        datos = DetallesVentasProductos(fecha)
 
    return render(request, "reportes/ventas_por_productos.html", {
        "form": form,
        "datos": list(datos),
        "titulo": "Ventas por producto",
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

@login_required
@permission_required('reportes.gestionar_reportes')
def VentasPorCategoria(request):
    import datetime
    from datetime import timedelta

    hoy = timezone.localdate()
    ayer = hoy - timedelta(days=1)

    fecha_inicio, fecha_fin = request.GET.get("fecha_inicio", ayer.strftime('%Y-%m-%d')), request.GET.get("fecha_fin", hoy.strftime('%Y-%m-%d'))
    form = PeriodoTiempoForm(initial={"fecha_inicio": fecha_inicio, "fecha_fin" : fecha_fin, })
    if "fecha_inicio" in request.GET:
        form = PeriodoTiempoForm(request.GET)
        if form.is_valid():
            total_de_ventas_por_categoria = VentasCategorias(fecha_inicio, fecha_fin)
        else:
            for campo, error in form.errors.items():
                messages.error(request, error[0])
            total_de_ventas_por_categoria = VentasCategorias(fecha_inicio, fecha_fin)
    else:
        total_de_ventas_por_categoria = VentasCategorias(fecha_inicio, fecha_fin)
    print(list(total_de_ventas_por_categoria))
    return render(request, "reportes/ventas_por_categorias.html", {
        "form": form,
        "total_de_ventas_por_categoria": total_de_ventas_por_categoria,
        "fecha_inicio": fecha_inicio,
        "fecha_fin" : fecha_fin,
        "datos": list(total_de_ventas_por_categoria),
        "titulo": "Ventas por categoría",
    })
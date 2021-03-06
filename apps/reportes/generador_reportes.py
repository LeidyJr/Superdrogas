from django.db import models
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate, TruncMonth
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from apps.medicamentos.models import Medicamento
from apps.ventas.models import Venta, VentaProducto

def DetallesVentas(fecha):
    ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True)).filter(fecha__date=fecha).order_by("-fecha").select_related("cliente", "trabajador").prefetch_related("productos_comprados", "productos_comprados__producto")
    return ventas

def DetallesVentasProductos(fecha):
    productos =  VentaProducto.objects.exclude(Q(venta__terminada=None) | Q(venta__cancelado=True)).\
        filter(venta__fecha__date=fecha).prefetch_related("producto").\
        values('producto').annotate(total=Sum('cantidad')).order_by('-total')
    
    productos = list(productos)
    for id_venta in range(len(productos)):
        id_producto = productos[id_venta]["producto"]
        productos[id_venta]["nombre"] = get_object_or_404(Medicamento, pk=id_producto).nombre
    return productos

def VentasDiarias(inicio="", fin=""):
    try:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True)).filter(fecha__gte=inicio, fecha__lte=fin)
    except ValidationError as e:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True))

    ventas = ventas.order_by() \
        .annotate(dia_venta=TruncDate('fecha', output_field=models.DateField())) \
        .values('dia_venta') \
        .annotate(total_venta=Sum('total')).order_by("dia_venta")
    
    ventas = list(ventas)
    for id_venta in range(len(ventas)):
        dia = ventas[id_venta]["dia_venta"]
        ventas[id_venta]["dia_venta"] = dia.strftime("%Y-%m-%d")
    print("------", ventas)
    return ventas

def VentasCategorias(inicio="", fin=""):

    total_de_ventas_por_categoria =  VentaProducto.objects.exclude(Q(venta__terminada=None) | Q(venta__cancelado=True)).\
        filter(venta__fecha__gte=inicio, venta__fecha__lte=fin).prefetch_related("producto__categoria").\
        values('producto__categoria__nombre').annotate(total=Sum(F('precio') * F('cantidad'))).order_by('producto__categoria__nombre')
        
    valor_total = list(total_de_ventas_por_categoria.aggregate(Sum('total')).values())[0]
    print(total_de_ventas_por_categoria)
    return total_de_ventas_por_categoria

def VentasClientes(inicio="", fin=""):

    total_de_ventas_por_cliente =  VentaProducto.objects.exclude(Q(venta__terminada=None) | Q(venta__cancelado=True)).\
        filter(venta__fecha__gte=inicio, venta__fecha__lte=fin).prefetch_related("venta__cliente").\
        values('venta__cliente__first_name').annotate(total=Sum('cantidad')).order_by('venta__cliente__first_name')
    print(total_de_ventas_por_cliente)
    valor_total = list(total_de_ventas_por_cliente.aggregate(Sum('total')).values())[0]
    print(total_de_ventas_por_cliente)
    return total_de_ventas_por_cliente


def VentasVendedores(inicio="", fin=""):

    total_de_ventas_por_vendedor =  VentaProducto.objects.exclude(Q(venta__terminada=None) | Q(venta__cancelado=True)| Q(venta__trabajador=None)).\
        filter(venta__fecha__gte=inicio, venta__fecha__lte=fin).prefetch_related("venta__trabajador").\
        values('venta__trabajador__first_name').annotate(total=Sum('cantidad')).order_by('venta__trabajador__first_name')
    print(total_de_ventas_por_vendedor)
    valor_total = list(total_de_ventas_por_vendedor.aggregate(Sum('total')).values())[0]
    print(total_de_ventas_por_vendedor)
    return total_de_ventas_por_vendedor

def VentasSitu(inicio="", fin=""):
    try:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True)| Q(trabajador=None)).filter(fecha__gte=inicio, fecha__lte=fin)
    except ValidationError as e:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True))

    ventas = ventas.order_by() \
        .annotate(dia_venta=TruncDate('fecha', output_field=models.DateField())) \
        .values('dia_venta').annotate(total=Count('total'))
    ventas = list(ventas)
    for id_venta in range(len(ventas)):
        dia = ventas[id_venta]["dia_venta"]
        ventas[id_venta]["dia_venta"] = dia.strftime("%Y-%m-%d")
    return ventas

def VentasOnline(inicio="", fin=""):
    try:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True)).filter(fecha__gte=inicio, fecha__lte=fin, trabajador=None)
    except ValidationError as e:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True))

    ventas = ventas.order_by() \
        .annotate(dia_venta=TruncDate('fecha', output_field=models.DateField())) \
        .values('dia_venta').annotate(total=Count('total'))
    ventas = list(ventas)
    for id_venta in range(len(ventas)):
        dia = ventas[id_venta]["dia_venta"]
        ventas[id_venta]["dia_venta"] = dia.strftime("%Y-%m-%d")
    return ventas


def VentasMensuales(inicio="", fin=""):
    from django.db.models.functions import Extract
    try:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True)).filter(fecha__gte=inicio, fecha__lte=fin)
    except ValidationError as e:
        ventas = Venta.objects.exclude(Q(terminada=None) | Q(cancelado=True))

    ventas = ventas.order_by() \
        .annotate(mes_venta=TruncMonth('fecha', output_field=models.DateField())) \
        .values('mes_venta') \
        .annotate(total_venta=Count('id')).order_by("mes_venta")
    
    for id_venta in range(len(ventas)):
        mes = ventas[id_venta]["mes_venta"]
        ventas[id_venta]["mes_venta"] = mes.strftime('%B')
    ventas = list(ventas)
    print("------", ventas)
    return ventas
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import DetailView, TemplateView
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.categorias.models import Categoria
from apps.core.permissions import NoClientePermission
from apps.medicamentos.models import Medicamento
from apps.ventas.models import Venta, VentaProducto, VentaCancelacion
from apps.usuarios.models import Usuario
from apps.ventas.forms import VentaProductoForm, SeleccionarClienteForm

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, NoClientePermission, ))
def nueva_venta(request, id_producto):
    producto = get_object_or_404(Medicamento, pk=id_producto)
    venta = Venta.obtener_venta(request)
    productos_carrito = venta.productos_comprados.filter(venta=venta, producto=id_producto).first()
    if producto.cantidad >= 1:
        if productos_carrito == None:
            vp = VentaProducto.objects.create(venta=venta, producto=producto, cantidad=1, precio=producto.precio, descuento=0)
            vp.venta.subtotal += producto.precio
            vp.venta.save()
            vp.save()
        else:
            vp = VentaProducto.objects.get(venta=venta, producto=producto)
            vp.cantidad +=1
            if vp.producto.cantidad >= vp.cantidad:
                vp.precio += producto.precio
                vp.venta.subtotal += producto.precio
                vp.venta.save()
                vp.save()
            else:
                messages.error(request, 'La cantidad seleccionada no está disponible. ')
    else:
        messages.error(request, 'La cantidad seleccionada no está disponible. ')
        return Response(["Error"])
    return redirect('categorias:inicio_ventas')

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, NoClientePermission, ))
def eliminar_producto_carrito(request, id_producto):
    venta_activa = Venta.obtener_venta(request)
    producto = get_object_or_404(VentaProducto, pk=id_producto)
    if producto in venta_activa.productos_comprados.all():
        producto.venta.subtotal -= producto.producto.precio*producto.cantidad
        producto.venta.save()
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
    else:
        return redirect("categorias:inicio_ventas")
    return redirect("categorias:inicio_ventas")

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, NoClientePermission, ))
def finalizar_venta(request):
    from django.db.models import Sum
    from django.db.models.functions import Coalesce

    empresa = request.tenant
    categorias = Categoria.objects.filter(empresa=request.tenant)
    activa = Venta.obtener_venta_activa(request, None, request.user)
    productos_carrito = activa.productos_comprados.all()
    if productos_carrito == None:
        return 0
    cantidad_carrito = productos_carrito.aggregate(cant_carrito=Coalesce(Sum("cantidad"),0))["cant_carrito"]
    productos_carrito = productos_carrito
    subtotal = activa.subtotal
    iva = subtotal*0.19
    total = subtotal + iva

    if request.method == 'POST':
        form = SeleccionarClienteForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            venta_activa = Venta.obtener_venta(request)
            venta_activa.cliente = cliente
            subtotal = venta_activa.subtotal
            venta_activa.iva = iva
            venta_activa.total = total
            venta_activa.terminada = timezone.now()
            venta_activa.save()
            for producto in productos_carrito:
                producto.producto.cantidad -= producto.cantidad
                producto.producto.verificar_disponibilidad()
                producto.producto.save()
            del request.session['venta_activa']
            messages.success(request, 'Venta realizada exitosamente.')#pendiente por resolver
            return redirect('categorias:inicio_ventas')
    else:
        form = SeleccionarClienteForm()
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/finalizar_venta.html', {
        'form': form,
        'venta_activa': venta_activa,
        'categorias':categorias,
        'activa': activa,
        'empresa': empresa,
        'productos_carrito': productos_carrito,
        'cantidad_carrito': cantidad_carrito,
        'subtotal': subtotal,
        'total': total,
        'iva':iva,
    })

#--------------------- Compras ---------------------------

def nueva_compra(request, id_producto):
    producto = get_object_or_404(Medicamento, pk=id_producto)
    venta = Venta.obtener_venta(request)
    productos_carrito = venta.productos_comprados.filter(venta=venta, producto=id_producto).first()
    if producto.cantidad >= 1:
        if productos_carrito == None:
            vp = VentaProducto.objects.create(venta=venta, producto=producto, cantidad=1, precio=producto.precio, descuento=0)
            vp.venta.subtotal += producto.precio
            vp.venta.save()
            vp.save()
        else:
            vp = VentaProducto.objects.get(venta=venta, producto=producto)
            vp.cantidad +=1
            if vp.producto.cantidad >= vp.cantidad:
                vp.precio += producto.precio
                vp.venta.subtotal += producto.precio
                vp.venta.save()
                vp.save()
            else:
                messages.error(request, 'La cantidad seleccionada no está disponible. ')
    else:
        messages.error(request, 'La cantidad seleccionada no está disponible. ')
    return redirect('categorias:inicio_compras')

def eliminar_producto_carrito_compra(request, id_producto):
    venta_activa = Venta.obtener_venta(request)
    producto = get_object_or_404(VentaProducto, pk=id_producto)
    if producto in venta_activa.productos_comprados.all():
        producto.venta.subtotal -= producto.producto.precio*producto.cantidad
        producto.venta.save()
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
    else:
        return redirect("categorias:inicio_compras")
    return redirect("categorias:inicio_compras")


def finalizar_compra(request):
    from django.db.models import Sum
    from django.db.models.functions import Coalesce

    empresa = request.tenant
    categorias = Categoria.objects.filter(empresa=request.tenant)
    activa = Venta.obtener_venta_activa(request, request.user, None)
    productos_carrito = activa.productos_comprados.all()
    if productos_carrito == None:
        return 0
    cantidad_carrito = productos_carrito.aggregate(cant_carrito=Coalesce(Sum("cantidad"),0))["cant_carrito"]
    productos_carrito = productos_carrito
    subtotal = activa.subtotal
    iva = subtotal*0.19
    total = subtotal + iva

    if request.method == 'POST':
        venta_activa = Venta.obtener_venta(request)
        subtotal = venta_activa.subtotal
        venta_activa.iva = iva
        venta_activa.total = total
        venta_activa.terminada = timezone.now()
        venta_activa.save()
        for producto in productos_carrito:
            producto.producto.cantidad -= producto.cantidad
            producto.producto.verificar_disponibilidad()
            producto.producto.save()
        del request.session['venta_activa']
        messages.success(request, 'Compra realizada exitosamente.')#pendiente por resolver
        return redirect('categorias:inicio_compras')
    else:
        pass
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/finalizar_venta.html', {
        'venta_activa': venta_activa,
        'categorias':categorias,
        'activa': activa,
        'empresa': empresa,
        'productos_carrito': productos_carrito,
        'cantidad_carrito': cantidad_carrito,
        'subtotal': subtotal,
        'total': total,
        'iva':iva,
    })

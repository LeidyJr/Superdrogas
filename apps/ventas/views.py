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

from apps.medicamentos.models import Medicamento
from apps.ventas.models import Venta, VentaProducto, VentaCancelacion
from apps.usuarios.models import Usuario
from apps.ventas.forms import VentaProductoForm, SeleccionarClienteForm


def nueva_venta(request, id_producto):
    producto = get_object_or_404(Medicamento, pk=id_producto)
    venta = Venta.obtener_venta(request)
    VentaProducto.objects.create(venta=venta, producto=producto, cantidad=1, precio=producto.precio, descuento=0)
    return redirect('categorias:inicio')

def eliminar_producto_carrito(request, id_producto):
    producto = get_object_or_404(Medicamento, pk=id_producto)
    producto.delete()
    return redirect('categorias:inicio')

def eliminar_producto_carrito(request, id_producto):
    venta_activa = Venta.obtener_venta(request)
    producto = get_object_or_404(VentaProducto, pk=id_producto)

    if producto in venta_activa.productos_comprados.all():
        producto.delete()
        messages.success(request, 'Boleto eliminado exitosamente.')
    return redirect("categorias:inicio")

def finalizar_venta(request):

    if request.method == 'POST':
        form = SeleccionarClienteForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            venta_activa = Venta.obtener_venta(request)
            venta_activa.cliente = cliente

            from django.db.models import Sum
            from django.db.models.functions import Coalesce

            productos_venta = venta_activa.productos_comprados.all()
            

            subtotal = productos_venta.aggregate(calc_subtotal=Coalesce(Sum("precio"),0))["calc_subtotal"]
            iva = subtotal*0.19
            total = subtotal + iva
            venta_activa.subtotal = subtotal
            venta_activa.iva = iva
            venta_activa.total = total
            venta_activa.terminada = True
            venta_activa.save()
            del request.session['venta_activa']
            messages.success(request, 'Venta realizada exitosamente.')
            #return redirect('ventas:factura', venta_activa.id)
    else:
        form = SeleccionarClienteForm()
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/finalizar.html', {
        'form': form,
        'venta_activa': venta_activa,
    })


    



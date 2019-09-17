from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.mixins import MensajeMixin
from apps.core.permissions import NoClientePermission
from apps.logs.mixins import LoggerFormMixin
from apps.logs.models import LogApp

from .models import Medicamento
from .forms import MedicamentoForm
from .serializers import MedicamentoSerializador

class Registrar(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamentos/registrar.html'
    success_url = reverse_lazy('medicamentos:listado')
    permission_required = ('medicamentos.gestionar_productos',)
    mensaje_log = "Registro de producto"
    mensaje_exito = "Producto registrado correctamente"
    mensaje_error = "Hubo un error en el formulario del producto"

    def form_valid(self, form):
        form.save()
        return super(Registrar, self).form_valid(form)

class Listado(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    context_object_name = "medicamentos"
    template_name = 'medicamentos/listado.html'
    permission_required = ('medicamentos.gestionar_productos',)

    def get_queryset(self):
        return Medicamento.obtener_listado()

class Modificar(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamentos/modificar.html'
    success_url = reverse_lazy('medicamentos:listado')
    permission_required = ('medicamentos.gestionar_productos',)
    mensaje_log = "Modificación de producto"
    mensaje_exito = "Producto modificado correctamente"
    mensaje_error = "Hubo un error en el formulario del producto"

class Consultar(View):
    def get(self, request, *args, **kwargs):
        from apps.categorias.models import Categoria
        from apps.ventas.models import Venta
        from django.db.models import Sum
        from django.db.models.functions import Coalesce
        
        producto = get_object_or_404(Medicamento, pk=kwargs['pk'])
        categorias = Categoria.objects.filter(empresa=self.request.tenant)
        productos = Medicamento.objects.filter(categoria__empresa=self.request.tenant, activo=True)
        venta_activa = Venta.obtener_venta_activa(self.request, None, self.request.user)
        productos_carrito = venta_activa.productos_comprados.all()
        if productos_carrito == None:
            return 0
        cantidad_carrito = productos_carrito.aggregate(cant_carrito=Coalesce(Sum("cantidad"),0))["cant_carrito"]
        productos_carrito = productos_carrito
        subtotal = venta_activa.subtotal
        context = {'producto': producto, 'categorias':categorias, 'productos':productos, 'venta_activa': venta_activa, 'productos_carrito':productos_carrito, 'cantidad_carrito': cantidad_carrito, 'subtotal':subtotal,}
        return render(request, 'medicamentos/consultar.html', context)

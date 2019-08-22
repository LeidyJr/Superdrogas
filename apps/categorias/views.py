from django.db.models import Count, Q
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from rest_framework.response import Response

from apps.core.mixins import MensajeMixin
from apps.logs.mixins import LoggerFormMixin
from apps.usuarios.models import Usuario
from apps.medicamentos.models import Medicamento
from apps.ventas.models import VentaProducto, Venta
from .models import Categoria
from .forms import RegistrarCategoriaForm
from .serializers import CategoriaSerializador

class APICategoria(generics.ListAPIView):
    queryset = Categoria.objects.annotate(total_productos=Count('productos', filter=Q(productos__activo=True))).filter(total_productos__gt=0)
    serializer_class = CategoriaSerializador

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CategoriaSerializador(queryset, many=True)
        return Response(serializer.data)

class Inicio(TemplateView):
    template_name = "categorias/inicio.html"

    def dispatch(self, request, *args, **kwargs):
        from django.http import Http404
        Usuario.crear_usuario_inicial()
        return super(Inicio, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        from django.db.models.functions import Coalesce

        context = super().get_context_data(**kwargs)
        context['empresa'] = self.request.tenant
        context['categorias'] = Categoria.objects.filter(empresa=self.request.tenant)
        context['productos'] = Medicamento.objects.filter(categoria__empresa=self.request.tenant, activo=True)
        venta_activa = Venta.obtener_venta_activa(self.request, None, self.request.user)#cambiar aqui
        productos_carrito = venta_activa.productos_comprados.all()
        if productos_carrito == None:
            return 0
        context['cantidad_carrito'] = productos_carrito.aggregate(cant_carrito=Coalesce(Sum("cantidad"),0))["cant_carrito"]
        context['productos_carrito'] = productos_carrito
        context['subtotal'] = venta_activa.subtotal
        return context

class RegistrarCategoria(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, CreateView):
    form_class = RegistrarCategoriaForm
    template_name = "categorias/registrar.html"
    success_url = reverse_lazy("categorias:registrar")
    permission_required = ('categorias.gestionar_categorias',)
    mensaje_log = "Registro de categoría de productos"
    mensaje_exito = "Categoría de productos registrada correctamente"
    mensaje_error = "Hubo un error en el formulario de la categoría de productos"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.empresa = self.request.tenant
        self.object.save()
        return super(RegistrarCategoria, self).form_valid(form)

class ModificarCategoria(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, UpdateView):
    model = Categoria
    form_class = RegistrarCategoriaForm
    template_name = "categorias/modificar.html"
    success_url = reverse_lazy("categorias:listado")
    permission_required = ('categorias.gestionar_categorias',)
    mensaje_log = "Modificación de categoría de productos"
    mensaje_exito = "Categoría de productos modificada correctamente"
    mensaje_error = "Hubo un error en el formulario de la categoría de productos"

class ListadoCategoria(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Categoria
    template_name = "categorias/listado.html"
    context_object_name = "listado_categorias"
    permission_required = ('categorias.gestionar_categorias',)


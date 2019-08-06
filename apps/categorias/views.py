from django.db.models import Count, Q
from django.views.generic import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from rest_framework.response import Response

from apps.core.mixins import MensajeMixin
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

class RegistrarCategoria(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, CreateView):
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

class ModificarCategoria(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, UpdateView):
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
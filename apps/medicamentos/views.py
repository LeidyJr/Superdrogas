from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
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

class Listado(LoginRequiredMixin, ListView):
    context_object_name = "medicamentos"
    template_name = 'medicamentos/listado.html'
    #permission_required = ('medicamentos.gestionar_productos',)

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
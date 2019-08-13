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

from .models import Lote
from .forms import LoteForm
from .serializers import LoteSerializador

class Registrar(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, CreateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lotes/registrar.html'
    success_url = reverse_lazy('lotes:listado')
    permission_required = ('lotes.gestionar_lotes',)
    mensaje_log = "Registro de lote"
    mensaje_exito = "Lote registrado correctamente"
    mensaje_error = "Hubo un error en el formulario del lote"

    def form_valid(self, form):
        form.save()
        return super(Registrar, self).form_valid(form)

class Listado(LoginRequiredMixin, ListView):
    context_object_name = "lotes"
    template_name = 'lotes/listado.html'
    #permission_required = ('medicamentos.gestionar_productos',)

    def get_queryset(self):
        return Lote.obtener_listado()

class Modificar(LoginRequiredMixin, PermissionRequiredMixin, LoggerFormMixin, MensajeMixin, UpdateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lotes/modificar.html'
    success_url = reverse_lazy('lotes:listado')
    permission_required = ('lotes.gestionar_lotes',)
    mensaje_log = "Modificación de lote"
    mensaje_exito = "Lote modificado correctamente"
    mensaje_error = "Hubo un error en el formulario del lote"
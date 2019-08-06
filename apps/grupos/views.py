from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.core.mixins import MensajeMixin
from .forms import GrupoForm 

class RegistrarGrupo(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, CreateView):
    model = Group
    form_class = GrupoForm
    template_name = "grupos/registrar.html"
    success_url = reverse_lazy("grupos:registrar")
    permission_required = ('grupos.gestionar_grupos',)
    mensaje_log = "Registro de grupo de usuarios"
    mensaje_exito = "Grupo de usuarios registrado correctamente"
    mensaje_error = "Hubo un error en el formulario de grupo de usuarios"

class ModificarGrupo(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, UpdateView):
    model = Group
    form_class = GrupoForm
    template_name = "grupos/modificar.html"
    success_url = reverse_lazy("grupos:listado")
    permission_required = ('grupos.gestionar_grupos',)
    mensaje_log = "Modificación de grupo de usuarios"
    mensaje_exito = "Grupo de usuarios modificado correctamente"
    mensaje_error = "Hubo un error en el formulario de grupo de usuarios"

    def get_object(self, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        obj = super(ModificarGrupo, self).get_object(*args, **kwargs)
        if obj.name == "Cliente":
            raise PermissionDenied
        return obj

class ListadoGrupo(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = "grupos/listado.html"
    context_object_name = "listado_grupos"
    permission_required = ('grupos.gestionar_grupos',)

    def get_queryset(self):
        return Group.objects.exclude(name="Cliente")
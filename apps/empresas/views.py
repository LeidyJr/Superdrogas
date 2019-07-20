from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.core.mixins import MensajeMixin

from .forms import RegistrarEmpresaForm, ModificarEmpresaForm
from .models import Empresa, Dominio

class RegistrarEmpresa(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, CreateView):
    form_class = RegistrarEmpresaForm
    template_name = "empresas/registrar.html"
    success_url = reverse_lazy("empresas:listado")
    permission_required = ('empresas.gestionar_empresas',)
    mensaje_log = "Registro de nueva empresa"
    mensaje_exito = "Empresa registrada correctamente"
    mensaje_error = "Hubo un error en el formulario de la empresa"

    def form_valid(self, form):
        from django.conf import settings
        
        self.object = form.save()
        dominio = Dominio.objects.create(
            domain = ("%s%s")%(self.object.schema_name, settings.DOMAIN),
            is_primary = True,
            tenant = self.object
        )
        return super(RegistrarEmpresa, self).form_valid(form)

class ModificarEmpresa(LoginRequiredMixin, PermissionRequiredMixin, MensajeMixin, UpdateView):
    model = Empresa
    form_class = ModificarEmpresaForm
    template_name = "empresas/modificar.html"
    success_url = reverse_lazy("empresas:listado")
    permission_required = ('empresas.gestionar_empresas',)
    mensaje_log = "Modificar empresa"
    mensaje_exito = "Empresa modificada correctamente"
    mensaje_error = "Hubo un error en el formulario de la empresa"

class ListadoEmpresa(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Empresa
    template_name = "empresas/listado.html"
    context_object_name = "listado_empresas"
    permission_required = ('empresas.gestionar_empresas',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listado_dominios'] = Dominio.objects.exclude(tenant__schema_name="public").select_related("tenant")
        return context
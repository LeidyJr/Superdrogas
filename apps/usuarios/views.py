from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, ListView, TemplateView, DetailView, RedirectView
from django.contrib.auth import authenticate, login, logout

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.core.utils import superuser_required

from .models import *
from .forms import *

class Login(FormView):
    form_class = LoginForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('medicamentos:listado')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("medicamentos:listado")
        return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        mensaje = ""
        usuario = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        if usuario is not None:
            if usuario.is_active:
                login(self.request, usuario)
                siguiente = self.request.GET.get("next", None)
                self.success_url = self.success_url if siguiente == None else siguiente
                messages.success(self.request, "Sesión iniciada correctamente")
                return super(Login, self).form_valid(form)
            else:
                mensaje = "El usuario %s no esta activo"%(usuario.username)
        else:
            mensaje = "El usuario no existe o la contraseña es incorrecta"
        form.add_error('username', mensaje)
        messages.error(self.request, mensaje)
        return super(Login, self).form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ingrese un usuario y una contraseña válido para acceder al sistema")
        return super(Login, self).form_invalid(form)

@login_required
def Logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('usuarios:login')

class Landing(TemplateView):
    template_name = "usuarios/inicio.html"
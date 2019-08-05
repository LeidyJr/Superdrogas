from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, ListView, TemplateView, DetailView, RedirectView
from django.contrib.auth import authenticate, login, logout

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.utils import superuser_required

from .serializers import UsuarioSerializador
from .models import *
from .forms import *

class Login(FormView):
    form_class = LoginForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("inicio")
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

@login_required
@permission_required('usuarios.gestionar_usuarios')
def RegistrarTrabajador(request, id_trabajador=None):
    usuario, trabajador = None, None
    mensaje_formulario = ["registro", "Registrar"]

    if id_trabajador:
        usuario = get_object_or_404(Usuario, pk=id_trabajador, rol="Trabajador")

        if usuario.email == "admin@gmail.com":
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        trabajador = usuario.obtener_datos_rol()
        mensaje_formulario = ["modificación", "Modificar"]

    form_usuario = UsuarioForm(instance=usuario)
    form_trabajador = TrabajadorForm(instance=trabajador)

    if request.method == "POST":
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        form_trabajador = TrabajadorForm(request.POST, instance=trabajador)

        if form_usuario.is_valid() and form_trabajador.is_valid():
            usuario = form_usuario.save()
            usuario.rol = "Trabajador"
            if id_trabajador == None:
                usuario.set_password("%s-%s"%(request.tenant.schema_name, usuario.email))
            usuario.save()

            trabajador = form_trabajador.save(commit=False)
            trabajador.usuario = usuario
            trabajador.save()

            messages.success(request, "Trabajador %s correctamente"%("registrado" if id_trabajador==None else "modificado"))
            return redirect("usuarios:listado")
        else:
            messages.error(request, "Hubo un error en el formulario del trabajador")

    return render(request, "usuarios/registrar_trabajador.html", {
        "form_usuario": form_usuario,
        "form_trabajador": form_trabajador,
        "mensaje_formulario": mensaje_formulario,
    })

class ListadoUsuarios(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = "usuarios/listado.html"
    context_object_name = "listado_usuarios"
    permission_required = ('usuarios.gestionar_usuarios',)

    def get_queryset(self):
        return Usuario.objects.exclude(email="admin@gmail.com")

@login_required
@permission_required('usuarios.gestionar_usuarios')
def DesactivarUsuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    usuario.is_active = False
    usuario.save()
    messages.success(request, "El usuario ha sido desactivado correctamente")
    return redirect('usuarios:listado')

@login_required
@permission_required('usuarios.gestionar_usuarios')
def ActivarUsuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    usuario.is_active = True
    usuario.save()
    messages.success(request, "El usuario ha sido activado correctamente")
    return redirect('usuarios:listado')

@login_required
@permission_required('usuarios.gestionar_usuarios')
@superuser_required
def AsignacionAdministrador(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if usuario.email != "admin@gmail.com":
        usuario.is_superuser = not(usuario.is_superuser)
        usuario.save()
        messages.success(request, "El usuario ahora %s administrador"%("es" if usuario.is_superuser else "no es"))
    return redirect('usuarios:listado')

class UsuarioListado(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UsuarioSerializador

    def get_queryset(self):
        return Usuario.objects.filter(rol="Cliente")
from django.contrib import messages
from django.shortcuts import render, redirect

from apps.usuarios.models import Usuario

def Inicio(request):
    Usuario.crear_grupos()
    Usuario.crear_usuario_inicial()
    configurar_llaves_acceso_redes_sociales()

    if request.tenant.schema_name == "public":
        if not request.user.is_authenticated:
            return redirect("landing")
        return redirect("empresas:listado")

    if request.user.is_authenticated:
        if request.user.rol=="Cliente":
            return redirect("categorias:inicio_compras")#cambiar x landing de la franquicia ("categorias:landing")
        else:
            return redirect("categorias:inicio_ventas")
    return redirect("usuarios:login")


def Landing(request):
    from django.conf import settings
    from django.core.mail import EmailMessage

    from .forms import ContactanosForm
    
    form = ContactanosForm()
    if request.method == "POST":
        form = ContactanosForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            mensaje = form.cleaned_data['mensaje']
            try:
                email = EmailMessage('Mensaje de contacto Superdrogas', '%s con correo electrónico %s cuyo teléfono es %s ha enviado el siguiente mensaje: %s'%(nombre, email, telefono, mensaje), to=['superdrogasfranquicias@gmail.com'])
                print(email)
                email.send()
                messages.success(request, "Mensaje enviado correctamente, muy pronto nos comunicaremos contigo")
            except Exception:
                messages.error(request, "Error al enviar el mensaje, por favor inténtelo más tarde")
            return redirect('landing')

    return render(request, "core/inicio.html", {
        "form": form,
    })

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_signed_up)
def usuario_logueado_red_social(sender, request, user, **kwargs):
    from django.contrib.auth.models import Group
    user.rol = "Cliente"
    user.save()
    grupo = Group.objects.get(name="Cliente")
    grupo.user_set.add(user)

def configurar_llaves_acceso_redes_sociales():
    from django.conf import settings
    from django.contrib.sites.models import Site
    from django.core.exceptions import MultipleObjectsReturned

    from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp

    try:
        SocialApp.objects.get(provider="google")
    except SocialApp.DoesNotExist:
        google = SocialApp.objects.create(provider="google", name="Google", client_id=settings.GOOGLE["CLIENT_ID"], secret=settings.GOOGLE["SECRET_KEY"])
        google.sites.add(Site.objects.first())
    except MultipleObjectsReturned:
        pass
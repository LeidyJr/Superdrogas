from django.contrib import messages
from django.shortcuts import render, redirect

from apps.usuarios.models import Usuario

def Inicio(request):
    Usuario.crear_grupos()
    Usuario.crear_usuario_inicial()

    if request.tenant.schema_name == "public":
        if not request.user.is_authenticated:
            return redirect("inicio")
        return redirect("empresas:listado")

    if not request.user.is_authenticated:
        return redirect("usuarios:login")#cambiar x landing de la franquicia ("categorias:landing")
    return redirect("medicamentos:listado")


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
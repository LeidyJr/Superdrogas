from django.contrib import messages
from django.shortcuts import render, redirect

from apps.usuarios.models import Usuario

def Inicio(request):
    

    if request.tenant.schema_name == "public":
        if not request.user.is_authenticated:
            return redirect("empresas:listado")
        return redirect("empresas:listado")

    if not request.user.is_authenticated:
        return redirect("medicamentos:listado")
    return redirect("medicamentos:listado")
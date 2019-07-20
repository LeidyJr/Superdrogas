from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.usuarios.views import Landing

urlpatterns = [
    path("", Landing.as_view(), name='inicio'),
    path('medicamentos/', include ('apps.medicamentos.urls', namespace='medicamentos')),
    path("usuarios/", include("apps.usuarios.urls", namespace="usuarios")),
] 
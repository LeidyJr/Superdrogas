from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views

from apps.core.views import Inicio, Landing

urlpatterns = [
	path("", Inicio, name='inicio'),
    path("inicio", Landing, name='landing'),
    path('medicamentos/', include ('apps.medicamentos.urls', namespace='medicamentos')),
    path("usuarios/", include("apps.usuarios.urls", namespace="usuarios")),
    path("grupos/", include("apps.grupos.urls", namespace="grupos")),
    path("categorias/", include("apps.categorias.urls", namespace="categorias")),
    path("ventas/", include("apps.ventas.urls", namespace="ventas")),
    path("reportes/", include("apps.reportes.urls", namespace="reportes")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r"^accounts/", include("allauth.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

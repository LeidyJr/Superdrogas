from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.core.views import Inicio, Landing

urlpatterns = [
	path("", Inicio, name='inicio'),
    path("inicio", Landing, name='landing'),
    path('medicamentos/', include ('apps.medicamentos.urls', namespace='medicamentos')),
    path("usuarios/", include("apps.usuarios.urls", namespace="usuarios")),
    path("grupos/", include("apps.grupos.urls", namespace="grupos")),
    path("categorias/", include("apps.categorias.urls", namespace="categorias")),
    path("lotes/", include("apps.lotes.urls", namespace="lotes")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

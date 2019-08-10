from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.urls import path

from apps.core.views import Inicio, Landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Inicio, name='inicio'),
    path("inicio", Landing, name='landing'),
    path("empresas/", include("apps.empresas.urls", namespace="empresas")),
    path("usuarios/", include("apps.usuarios.urls", namespace="usuarios")),
    path("medicamentos/", include("apps.medicamentos.urls", namespace="medicamentos")),
    path("accounts/", include("allauth.urls")),
    path('select2/', include('django_select2.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

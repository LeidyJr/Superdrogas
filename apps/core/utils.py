from django.contrib.auth.decorators import user_passes_test
from django.db import connection

from datetimewidget.widgets import DateWidget, TimeWidget, DateTimeWidget

def MyDateWidget():
    return DateWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd', 'startView':4, 'language':'es'})

def MyDateTimeWidget():
    return DateTimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd HH:ii', 'startView':4, 'language':'es'})

def comprimir_imagen(nombre, ruta=None):
    from django.conf import settings

    from PIL import Image

    if not ruta:
        ruta = settings.MEDIA_ROOT
    
    imagen = Image.open(("%s/%s")%(ruta, nombre))
    imagen.save(("%s/%s")%(ruta, nombre), format=imagen.format, quality=70)

def campos_del_modelo_diligenciados(modelo, campos):
    for campo in campos:
        try:
            if getattr(modelo, campo) == None:
                return False
        except AttributeError:
            return False
    return True

def ejecutar_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)

def cambiar_de_empresa(empresa=None):
    from django.db import connection
    if empresa:
        connection.set_tenant(empresa)
    else:
        connection.set_schema_to_public()

def superuser_required(view_func=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def obtener_consulta_orden_ids(modelo, orden):
    from django.db.models import Case, When
    orden_preservado = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(orden)])
    consulta = modelo.objects.filter(pk__in=orden).order_by(orden_preservado)
    return consulta

def agregar_por(datos, operacion, columna):
    return datos.aggregate(agregado=operacion(columna))['agregado']
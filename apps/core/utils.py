from django.contrib.auth.decorators import user_passes_test
from django.db import connection

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
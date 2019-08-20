from django.db import models

class GruposPermisos(models.Model):
    class Meta:
        managed = False
        permissions = ( 
            ("gestionar_grupos", "Gestión de grupos de usuarios"),
        )
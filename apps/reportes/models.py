from django.db import models

class ReportesPermisos(models.Model):
    class Meta:
        managed = False
        permissions = ( 
            ("gestionar_reportes", "Gestión de reportes"),
        )
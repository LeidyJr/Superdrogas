from django.db import models

from apps.usuarios.models import Usuario

class Medicamento(models.Model):

	referencia = models.CharField(max_length=50, verbose_name="Referencia ")
	nombre = models.CharField(max_length=50, verbose_name="Nombre ")
	activo = models.BooleanField(default=True, verbose_name="¿El medicamento está activo actualmente?")

	class Meta:
		ordering = ["nombre"]

	def __str__(self):
		return ("%s"%(self.nombre))

	@staticmethod
	def obtener_listado():
		return Medicamento.objects.all()

	@staticmethod
	def existe_medicamento_activo():
		return Medicamento.obtener_activos().exists()

	@staticmethod
	def obtener_activos():
		return Medicamento.objects.filter(activo=True)

	def cambiar_estado(self):
		self.activo = not(self.activo)
		self.save()

	def obtener_estado(self):
		if self.activo:
			return "Activo"
		return "Inactivo"
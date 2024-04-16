from django.db import models

class Bafle(models.Model):
	marca  = models.CharField(max_length=50, null=False, blank=True)
	tamaño = models.CharField(max_length=50, null=False, blank=True)
	color  = models.CharField(max_length=50, null=False, blank=True)
	precio = models.IntegerField()
	def __str__(self):
		return self.marca	
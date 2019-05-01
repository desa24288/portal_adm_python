from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse

class Sector(models.Model):
	nom_sector = models.CharField(max_length=50)

class Company(models.Model):
	nombre = models.CharField(max_length=50)
	direccion = models.CharField(max_length=100)
	ciudad = models.CharField(max_length=50)
	telefono = models.CharField(max_length=50)
	web = models.CharField(max_length=50)
	sector = models.ForeignKey(Sector, on_delete=models.PROTECT)

	def __str__(self):
		return self.nombre

class Division(models.Model):
	nombre = models.CharField(max_length=50)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Planta(models.Model):
	nombre = models.CharField(max_length=50)
	division = models.ForeignKey(Division, on_delete=models.CASCADE)


class Area(models.Model):
	nombre = models.CharField(max_length=50)
	planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

class Categoria(models.Model):
	nombre = models.CharField(max_length=50)

class Tipo(models.Model):
	nombre = models.CharField(max_length=50)
	categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)


class Equipo(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	coste = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	peso = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	volumen = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	cantidad = models.IntegerField()
	tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
	area = models.ForeignKey(Area, on_delete=models.PROTECT)

	def __str__(self):
		return self.nombre

class Tecnica(models.Model):
	nombre = models.CharField(max_length=50)
	equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

class Actividad(models.Model):
	nombre = models.CharField(max_length=50)
	tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE)

class Sistema(models.Model):
	nombre = models.CharField(max_length=50)
	actividad = models.ForeignKey(Actividad, on_delete=models.PROTECT)

class Componente(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	espesor_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	espesor_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	espesor_nominal = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	espesor_retiro = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	espesor_permitida = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.0'))
	equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
	sistema = models.ForeignKey(Sistema, on_delete=models.PROTECT)

	def __str__(self):
		return self.nombre

class SubComponente(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	componente = models.ForeignKey(Componente, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre

class Modo_Falla(models.Model):
	nombre = models.CharField(max_length=100)
	subComponente = models.ForeignKey(SubComponente, on_delete=models.CASCADE)





from django.db import models
from users.models import Usuario


class Vehiculo(models.Model):
    TIPO_COMBUSTIBLE_CHOICES = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )
    matricula = models.CharField(max_length=50, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    tipo_combustible = models.CharField(
        max_length=20,
        choices=TIPO_COMBUSTIBLE_CHOICES
    )
    anyo_compra = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['marca', 'modelo', 'matricula']

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.matricula})"


class FotoVehiculo(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    imagen = models.ImageField(upload_to='vehiculos/')

    def __str__(self):
        return f"Foto de {self.vehiculo.matricula}"

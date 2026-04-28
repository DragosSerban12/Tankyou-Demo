from django.db import models
from users.models import Usuario
from vehicles.models import Vehiculo

class Turno(models.Model):
    fecha = models.DateField(verbose_name='Fecha')
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    capacidad_max = models.IntegerField(verbose_name='Capacidad máxima')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'hora_inicio', 'hora_fin'], 
                name='unique_turno'
            )
        ]

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ['fecha', 'hora_inicio']
        constraints = [
            models.UniqueConstraint(fields=['fecha', 'hora_inicio', 'hora_fin'], name='unique_turno')
        ]

    def __str__(self):
        return f"Turno {self.fecha} ({self.hora_inicio}-{self.hora_fin})"


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('error', 'Error'),
    ]

    usuario = models.ForeignKey(verbose_name='Usuario', to=Usuario, on_delete=models.CASCADE, related_name='pedidos')
    vehiculo = models.ForeignKey(verbose_name='Vehículo', to=Vehiculo, on_delete=models.CASCADE)
    turno = models.ForeignKey(verbose_name='Turno', to=Turno, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido = models.DateField(verbose_name='Fecha de pedido', auto_now_add=True)
    fecha_servicio = models.DateField(verbose_name='Fecha de servicio', null=True, blank=True)
    hora_servicio = models.TimeField(verbose_name='Hora de servicio', null=True, blank=True)
    ubicacion = models.CharField(verbose_name='Ubicación', max_length=200)
    cantidad_litros = models.DecimalField(verbose_name='Cantidad de litros', max_digits=5, decimal_places=2)
    precio_total = models.DecimalField(verbose_name='Precio total', max_digits=8, decimal_places=2)
    estado = models.CharField(verbose_name='Estado', max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario}"
from django.db import models
from orders.models import Pedido

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('aprobado', 'Aprobado'),
        ('pendiente', 'Pendiente'),
        ('reembolsado', 'Reembolsado'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pago')
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    importe = models.DecimalField(max_digits=8, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago #{self.id} - {self.estado_pago}"


class Reembolso(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    pago = models.OneToOneField(verbose_name='Pago', to=Pago, on_delete=models.CASCADE, related_name='reembolso')
    motivo = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        verbose_name = "Reembolso"
        verbose_name_plural = "Reembolsos"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Reembolso #{self.id} - {self.estado}"
from django.db import models
from users.models import Usuario
from orders.models import Pedido

class Notificacion(models.Model):
    usuario = models.ForeignKey(verbose_name='Usuario', to=Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    pedido = models.ForeignKey(verbose_name='Pedido', to=Pedido, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(verbose_name='Tipo', max_length=50)
    mensaje = models.TextField(verbose_name='Mensaje')
    fecha_envio = models.DateTimeField(verbose_name='Fecha de envío', auto_now_add=True)
    leido = models.BooleanField(verbose_name='Leído', default=False)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_envio']
        constraints = [
            models.UniqueConstraint(fields=['pedido', 'tipo'], name='unique_tipo_por_pedido')
        ]

    def __str__(self):
        return f"Notificación a {self.usuario} - {self.tipo}"
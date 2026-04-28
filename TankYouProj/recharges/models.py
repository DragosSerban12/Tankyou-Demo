from django.db import models

class Recarga(models.Model):
    TIPO_COMBUSTIBLE_CHOICES = [
        ('gasolina_95', 'Gasolina 95'),
        ('gasolina_98', 'Gasolina 98'),
        ('diesel', 'Diésel'),
    ]

    tipo_combustible = models.CharField(verbose_name='Tipo de combustible', max_length=20, choices=TIPO_COMBUSTIBLE_CHOICES)
    precio_por_litro = models.DecimalField(verbose_name='Precio por litro', max_digits=5, decimal_places=2)
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    activo = models.BooleanField(verbose_name='Activo', default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_combustible'], 
                name='unique_tipo_combustible'
            )
        ]

    class Meta:
        verbose_name = "Recarga"
        verbose_name_plural = "Recargas"
        ordering = ['tipo_combustible']

    def __str__(self):
        return f"{self.get_tipo_combustible_display()} - {self.precio_por_litro} €/L"

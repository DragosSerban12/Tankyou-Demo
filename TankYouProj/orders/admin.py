from django.contrib import admin
from .models import Turno, Pedido

class TurnoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'capacidad_max')  # Campos visibles en la lista
    list_filter = ('fecha',)  # Permite filtrar por fecha

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vehiculo', 'fecha_servicio', 'estado')  # Campos mostrados en la tabla del admin
    search_fields = ('usuario__nombre', 'vehiculo__matricula')  # Búsqueda por usuario o matrícula
    list_filter = ('estado', 'fecha_servicio')  # Filtros laterales

admin.site.register(Turno, TurnoAdmin)
admin.site.register(Pedido, PedidoAdmin)
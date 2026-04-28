from django.contrib import admin
from .models import Notificacion

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'fecha_envio', 'leido')  # Campos visibles en el listado del admin
    list_filter = ('tipo', 'leido')  # Filtros laterales por tipo y si está leído
    search_fields = ('usuario__nombre', 'tipo', 'mensaje')  # Permite buscar por usuario, tipo o mensaje

admin.site.register(Notificacion, NotificacionAdmin)
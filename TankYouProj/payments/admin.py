from django.contrib import admin
from .models import Pago, Reembolso

class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'metodo_pago', 'importe', 'estado_pago')  # Campos mostrados en el listado
    search_fields = ('pedido__id', 'estado_pago')  # Permite buscar por pedido o estado

class ReembolsoAdmin(admin.ModelAdmin):
    list_display = ('pago', 'estado', 'fecha_solicitud')  # Campos visibles en el listado
    list_filter = ('estado',)  # Filtro por estado del reembolso

admin.site.register(Pago, PagoAdmin)
admin.site.register(Reembolso, ReembolsoAdmin)
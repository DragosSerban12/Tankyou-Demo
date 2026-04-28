from django.contrib import admin
from .models import Recarga

class RecargaAdmin(admin.ModelAdmin):
    list_display = ('tipo_combustible', 'precio_por_litro', 'activo')  # Campos visibles en el listado
    search_fields = ('tipo_combustible',)  # Permite buscar por tipo de combustible
    list_filter = ('activo', 'tipo_combustible')  # Filtros laterales

admin.site.register(Recarga, RecargaAdmin)
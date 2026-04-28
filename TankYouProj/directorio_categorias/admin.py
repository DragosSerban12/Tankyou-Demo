from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Subcategoria, Asociacion, Milistado

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Muestra campos principales en la tabla del admin
    search_fields = ('nombre',)  # Permite buscar por nombre


class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')  # Muestra subcategoría y su categoría vinculada
    list_filter = ('categoria',)  # Filtro lateral por categoría
    search_fields = ('nombre',)  # Buscar por nombre


class AsociacionAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'subcategoria')  # Muestra la relación categoría–subcategoría
    list_filter = ('categoria',)  # Filtro lateral por categoría


class MilistadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'subcategoria')  # Campos visibles del listado
    search_fields = ('titulo',)  # Permite buscar listados por título
    list_filter = ('categoria', 'subcategoria')  # Filtros laterales por categoría y subcategoría


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Subcategoria, SubcategoriaAdmin)
admin.site.register(Asociacion, AsociacionAdmin)
admin.site.register(Milistado, MilistadoAdmin)
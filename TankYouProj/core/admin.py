from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Modelo1, Modelo2, Modelo3

class Modelo1Admin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Campos visibles en la tabla del admin
    search_fields = ('nombre',)  # Permite buscar por nombre


class Modelo2Admin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_creacion')  # Muestra título y fecha
    list_filter = ('fecha_creacion',)  # Filtro lateral por fecha


class Modelo3Admin(admin.ModelAdmin):
    list_display = ('codigo', 'activo')  # Muestra código y si está activo
    search_fields = ('codigo',)  # Permite buscar por código
    list_filter = ('activo',)  # Filtro lateral por estado activo/inactivo


# Registro de los modelos en el panel de administración
admin.site.register(Modelo1, Modelo1Admin)
admin.site.register(Modelo2, Modelo2Admin)
admin.site.register(Modelo3, Modelo3Admin)
from django.contrib import admin
from .models import Vehiculo, FotoVehiculo


class FotoVehiculoInline(admin.TabularInline):
    model = FotoVehiculo
    extra = 0


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca', 'modelo', 'usuario')
    inlines = [FotoVehiculoInline]

from rest_framework import serializers
from vehicles.models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'usuario',
            'matricula',
            'modelo',
            'marca',
            'color',
            'tipo_combustible',
            'anyo_compra',
        ]
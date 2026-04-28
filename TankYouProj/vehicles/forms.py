from django import forms
from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'matricula',
            'marca',
            'modelo',
            'anyo_compra',
            'color',
            'tipo_combustible',
        ]

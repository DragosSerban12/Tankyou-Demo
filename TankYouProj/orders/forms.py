from django import forms
from .models import Pedido, Turno
from vehicles.models import Vehiculo

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['vehiculo', 'turno', 'cantidad_litros', 'ubicacion']
        widgets = {
            'turno': forms.HiddenInput(),
            'ubicacion': forms.TextInput(attrs={'placeholder': 'Ej. Calle Mayor 1, Madrid'}),
            'cantidad_litros': forms.NumberInput(attrs={'min': '1', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(usuario=user)
        
        from datetime import date
        from django.db.models import Count
        self.fields['turno'].queryset = Turno.objects.filter(
            fecha__gte=date.today()
        ).annotate(
            num_pedidos=Count('pedido')
        ).filter(
            num_pedidos__lt=5 # O usar F('capacidad_max')
        )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

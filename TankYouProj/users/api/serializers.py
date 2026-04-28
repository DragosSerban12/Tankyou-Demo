from rest_framework import serializers
from users.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'nombre',
            'apellidos',
            'email',
            'fecha_nacimiento',
            'dni',
            'direccion',
            'telefono',
            'verificado',
            'is_active',
            'is_admin',
            'is_staff',
            'create_date',
            'update_date',
        ]
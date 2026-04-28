from users.models import Usuario
from vehicles.models import Vehiculo
from faker import Faker
import random

fake = Faker('es_ES')

def crear_usuarios(n):
    for _ in range(n):
        user = Usuario.objects.create(
            nombre=fake.first_name(),
            apellidos=fake.last_name(),
            email=fake.email(),
            contrasenya=fake.password(),
            dni=fake.ssn(),
            fecha_nacimiento=fake.date_of_birth(),
            direccion=fake.address(),
            telefono=fake.phone_number()[:15],
            verificado=random.choice([True, False]),
        )

fake2 = Faker('es_ES')

def crear_vehiculos(n):
    for _ in range(n):
        vehicle = Vehiculo.objects.create(
            Usuario=random.choice(Usuario.objects.all()),
            matricula=fake2.license_plate(),
            modelo=fake2.vehicle_model(),
            marca=fake2.vehicle_brand(),
            color=fake2.color_name(),
            tipo_combustible=random.choice(['gasolina', 'diesel'])
        )
        
# Para ejecutar este script, hay que irse al bash del proyecto y ejecutar: python manage.py shell
# Luego, ejecutar: from common.simulador import crear_usuarios; 
# Luego ejecutar: crear_usuarios(10) / 10 es el número de usuarios que queremos crear  
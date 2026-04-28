from django.core.management.base import BaseCommand
from orders.models import Turno
from datetime import date, time, timedelta

class Command(BaseCommand):
    help = 'Carga los turnos de servicio de 05:00 a 21:00 con capacidad 5'

    def handle(self, *args, **kwargs):
        start_date = date.today()
        # Generar turnos para los próximos 7 días
        for day_offset in range(14):
            fecha = start_date + timedelta(days=day_offset)
            
            # De 05:00 a 21:00
            for hour in range(5, 21):
                hora_inicio = time(hour, 0)
                hora_fin = time(hour + 1, 0)
                
                turno, created = Turno.objects.get_or_create(
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    defaults={'capacidad_max': 5}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Turno creado: {fecha} {hora_inicio}-{hora_fin}'))
                else:
                    self.stdout.write(f'Turno ya existe: {fecha} {hora_inicio}-{hora_fin}')

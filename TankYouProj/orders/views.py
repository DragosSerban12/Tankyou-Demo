from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Pedido, Turno
from .forms import PedidoForm
from recharges.models import Recarga
from notifications.models import Notificacion
from decimal import Decimal

class OrdersHomeView(TemplateView):
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['pedidos'] = Pedido.objects.filter(usuario=self.request.user)
        else:
            context['pedidos'] = Pedido.objects.none()
        context['turnos'] = Turno.objects.all()
        return context

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'order_form.html'
    success_url = reverse_lazy('checkout')

    def ensure_turnos_for_range(self, start_date, days=7):
        from .models import Turno
        from datetime import time, timedelta
        
        for day_offset in range(days):
            fecha = start_date + timedelta(days=day_offset)
            for hour in range(5, 21):
                hora_inicio = time(hour, 0)
                hora_fin = time(hour + 1, 0)
                
                Turno.objects.get_or_create(
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    defaults={'capacidad_max': 5}
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from datetime import date, timedelta, datetime
        from django.db.models import Count, Q
        
        ahora = datetime.now()
        hoy = date.today()
        proximos_7_dias = [hoy + timedelta(days=i) for i in range(7)]
        
        # Asegurar que existan turnos para los próximos 7 días
        self.ensure_turnos_for_range(hoy, 7)
        
        # Obtener todos los turnos para los próximos 7 días con su contador de pedidos
        turnos = Turno.objects.filter(
            fecha__range=[hoy, hoy + timedelta(days=6)]
        ).annotate(
            num_pedidos=Count('pedido', filter=Q(pedido__estado__in=['pendiente', 'en_proceso', 'completado']))
        ).order_by('fecha', 'hora_inicio')
        
        # Agrupar por hora y día
        # horararios: lista de horas (de 5 a 20)
        horas = range(5, 21)
        grid = []
        for h in horas:
            fila = {'hora': f"{h:02d}:00", 'slots': []}
            for d in proximos_7_dias:
                # Buscar el turno para este día y hora
                turno = next((t for t in turnos if t.fecha == d and t.hora_inicio.hour == h), None)
                plazas_libres = (turno.capacidad_max - turno.num_pedidos) if turno else 0
                
                # Un slot es disponible si:
                # 1. El turno existe
                # 2. Hay plazas libres
                # 3. Si es hoy, la hora de inicio es posterior a la actual
                es_futuro = (d > hoy) or (d == hoy and h > ahora.hour)
                
                slot = {
                    'fecha': d,
                    'turno': turno,
                    'disponible': turno and plazas_libres > 0 and es_futuro,
                    'plazas_libres': plazas_libres,
                    'capacidad_total': turno.capacidad_max if turno else 0
                }
                fila['slots'].append(slot)
            grid.append(fila)
            
        context['proximos_7_dias'] = proximos_7_dias
        context['turno_grid'] = grid
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        pedido = form.save(commit=False)
        pedido.usuario = self.request.user
        
        # Obtener precio según combustible del vehículo
        combustible = pedido.vehiculo.tipo_combustible
        try:
            tipo_recarga = combustible
            if combustible == 'gasolina':
                tipo_recarga = 'gasolina_95'
            recarga = Recarga.objects.get(tipo_combustible=tipo_recarga)
            precio_litro = recarga.precio_por_litro
        except Recarga.DoesNotExist:
            precio_litro = Decimal('1.50')
            
        precio_total = Decimal(str(precio_litro)) * pedido.cantidad_litros
        
        fecha_servicio = pedido.turno.fecha if pedido.turno else None
        hora_servicio = str(pedido.turno.hora_inicio) if pedido.turno else None

        # Guardar datos del pedido en sesión para el checkout
        self.request.session['pedido_pendiente'] = {
            'vehiculo_id': pedido.vehiculo.id,
            'vehiculo_str': str(pedido.vehiculo),
            'turno_id': pedido.turno.id if pedido.turno else None,
            'turno_str': str(pedido.turno) if pedido.turno else '',
            'fecha_servicio': str(fecha_servicio),
            'hora_servicio': hora_servicio,
            'ubicacion': pedido.ubicacion,
            'cantidad_litros': str(pedido.cantidad_litros),
            'precio_total': str(precio_total),
        }

        return redirect(self.success_url)

class OrderCancelView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        from django.shortcuts import get_object_or_404
        from django.contrib import messages
        
        pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
        
        if pedido.estado == 'pendiente':
            pedido.estado = 'cancelado'
            pedido.save()
            
            # Crear notificación de cancelación
            from notifications.models import Notificacion
            Notificacion.objects.create(
                usuario=pedido.usuario,
                pedido=pedido,
                tipo='alerta',
                mensaje=f'Has cancelado el pedido #{pedido.id} para el día {pedido.fecha_servicio.strftime("%d/%m/%Y")}.'
            )
            
            messages.success(request, f"Pedido #{pk} cancelado correctamente.")
        else:
            messages.error(request, "Solo se pueden cancelar pedidos en estado pendiente.")
            
        return redirect('orders')
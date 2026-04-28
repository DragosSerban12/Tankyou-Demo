from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Pago, Reembolso
from orders.models import Pedido, Turno
from notifications.models import Notificacion
from decimal import Decimal


class PaymentsHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagos'] = Pago.objects.filter(pedido__usuario=self.request.user)
        context['reembolsos'] = Reembolso.objects.filter(pago__pedido__usuario=self.request.user)
        return context


class PaymentCheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):
        pedido_data = request.session.get('pedido_pendiente')
        if not pedido_data:
            messages.error(request, 'No hay ningún pedido pendiente de pago.')
            return redirect('order_create')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedido_data'] = self.request.session.get('pedido_pendiente', {})
        return context


class PaymentProcessView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pedido_data = request.session.get('pedido_pendiente')
        if not pedido_data:
            messages.error(request, 'Sesión expirada. Por favor, vuelve a crear el pedido.')
            return redirect('order_create')

        # Obtener el turno si existe
        turno = None
        if pedido_data.get('turno_id'):
            try:
                turno = Turno.objects.get(pk=pedido_data['turno_id'])
            except Turno.DoesNotExist:
                pass

        # Crear el pedido en la base de datos
        from vehicles.models import Vehiculo
        vehiculo = get_object_or_404(Vehiculo, pk=pedido_data['vehiculo_id'])

        fecha_servicio_raw = pedido_data.get('fecha_servicio')
        fecha_servicio = None if (not fecha_servicio_raw or fecha_servicio_raw == 'None') else fecha_servicio_raw

        pedido = Pedido.objects.create(
            usuario=request.user,
            vehiculo=vehiculo,
            turno=turno,
            fecha_servicio=fecha_servicio,
            hora_servicio=turno.hora_inicio if turno else None,
            ubicacion=pedido_data['ubicacion'],
            cantidad_litros=Decimal(pedido_data['cantidad_litros']),
            precio_total=Decimal(pedido_data['precio_total']),
            estado='pendiente',
        )

        # Crear el pago
        Pago.objects.create(
            pedido=pedido,
            metodo_pago='tarjeta',
            importe=Decimal(pedido_data['precio_total']),
            estado_pago='aprobado',
        )

        # Crear notificación
        from datetime import date
        try:
            fecha_str = pedido.fecha_servicio.strftime("%d/%m/%Y") if pedido.fecha_servicio else "sin fecha"
        except AttributeError:
            fecha_str = str(pedido.fecha_servicio) if pedido.fecha_servicio else "sin fecha"
        Notificacion.objects.create(
            usuario=request.user,
            pedido=pedido,
            tipo='info',
            mensaje=f'Pago confirmado para el pedido del día {fecha_str}. Importe: {pedido.precio_total} €. El pedido está pendiente de servicio.',
        )

        # Limpiar sesión
        del request.session['pedido_pendiente']

        return redirect('order_confirmation', pk=pedido.pk)


class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido = get_object_or_404(Pedido, pk=self.kwargs['pk'], usuario=self.request.user)
        context['pedido'] = pedido
        context['pago'] = getattr(pedido, 'pago', None)
        return context
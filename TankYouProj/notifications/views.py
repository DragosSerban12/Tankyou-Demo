from django.views.generic import TemplateView
from .models import Notificacion

class NotificationsHomeView(TemplateView):
    template_name = 'notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['notificaciones'] = Notificacion.objects.filter(usuario=self.request.user)
        else:
            context['notificaciones'] = Notificacion.objects.none()
        return context

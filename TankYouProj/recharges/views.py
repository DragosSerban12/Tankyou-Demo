from django.views.generic import TemplateView
from .models import Recarga

class RechargesHomeView(TemplateView):
    template_name = 'recharges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recargas'] = Recarga.objects.all()
        return context
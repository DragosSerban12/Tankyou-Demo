from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Vehiculo, FotoVehiculo
from .forms import VehiculoForm


class VehiclesCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehicles/Vehiculo_form.html'
    success_url = reverse_lazy('vehicles')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        fotos = self.request.FILES.getlist('fotos')

        if len(fotos) < 4 or len(fotos) > 10:
            form.add_error(None, 'Debes subir entre 4 y 10 fotos')
            return self.form_invalid(form)

        for foto in fotos:
            FotoVehiculo.objects.create(
                vehiculo=self.object,
                imagen=foto
            )

        return response


class VehiclesUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy('vehicles')
    login_url = 'login'


class VehiclesDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehiculo
    success_url = reverse_lazy('vehicles')
    login_url = 'login'


class VehiclesHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'vehicles.html'
    paginate_by = 6
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        vehiculos = Vehiculo.objects.filter(usuario=self.request.user)

        paginator = Paginator(vehiculos, self.paginate_by)
        page_obj = paginator.get_page(page)

        context["vehiculos"] = page_obj
        context["page_obj"] = page_obj

        return context


class VehiculoFotosView(LoginRequiredMixin, TemplateView):
    template_name = 'vehicles/vehiculo_fotos.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehiculo = get_object_or_404(
            Vehiculo,
            pk=self.kwargs['pk'],
            usuario=self.request.user
        )

        context['vehiculo'] = vehiculo
        context['fotos'] = vehiculo.fotos.all()

        return context

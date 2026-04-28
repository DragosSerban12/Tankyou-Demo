from datetime import date, timedelta
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UsuarioForm, UsuarioUpdateForm
from .models import Usuario
from vehicles.models import Vehiculo
from orders.models import Pedido
from payments.models import Pago
from recharges.models import Recarga
from notifications.models import Notificacion


# CRUD USUARIO
class UserCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        user = form.save(commit=False)  # guarda el objeto sin enviarlo aún a la BD
        user.set_password(form.cleaned_data['password'])  # encripta la contraseña
        user.save()
        return redirect(self.success_url)


class ProyectoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    success_url = reverse_lazy('Home')
    login_url = 'account_login'

    def test_func(self):
        # solo permite editar si el usuario logueado es el mismo que se está editando
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return redirect('Home')

    def form_valid(self, form):
        user = form.save(commit=False)

        password = form.cleaned_data.get('password')
        if password:  # si se introduce nueva contraseña, se vuelve a encriptar
            user.set_password(password)

        user.save()
        return redirect(self.success_url)


class ProyectoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('Home')
    login_url = 'account_login'

    def test_func(self):
        # solo puede eliminar su propio usuario
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return redirect('Home')


# LISTADO USUARIOS
class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = "users.html"
    paginate_by = 5
    context_object_name = "usuarios"  # nombre que se usará en el template
    login_url = 'account_login'

    def test_func(self):
        # solo staff puede ver el listado completo
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('Home')


class UsersHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'
    login_url = 'account_login'


# HOME (Landing pública)
class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        # si el usuario ya está logueado lo manda al dashboard
        if request.user.is_authenticated:
            return redirect('vista_usuario')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        letras = self.request.GET.get('letras')  # filtro por búsqueda

        if letras:
            context['usuarios'] = Usuario.objects.filter(nombre__icontains=letras)
        else:
            context['usuarios'] = Usuario.objects.all()

            marcado_vista = self.request.GET.get('marcado')  # parámetro para ordenar
            if marcado_vista == 'True':
                context['usuarios'] = context['usuarios'].order_by('nombre')

            context['marcado'] = marcado_vista

        return context


# LOGIN
from allauth.account.views import LoginView

class LoginFormView(LoginView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        # evita que un usuario logueado vea el login
        if request.user.is_authenticated:
            return redirect('vista_usuario')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('vista_usuario')


# DASHBOARD USUARIO
class VistaUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'vista_usuario.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user  # usuario actual logueado

        context['vehiculos'] = Vehiculo.objects.filter(usuario=usuario)

        # últimos 5 pedidos del usuario
        context['pedidos'] = Pedido.objects.filter(
            usuario=usuario
        ).order_by('-fecha_pedido')[:5]

        # contadores para mostrar estadísticas en el dashboard
        context['total_pedidos'] = Pedido.objects.filter(
            usuario=usuario
        ).count()

        context['total_vehiculos'] = Vehiculo.objects.filter(
            usuario=usuario
        ).count()

        return context
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import UsuarioSerializer
from users.models import Usuario
from .paginator import paginador_customizado


# ViewSet que SOLO permite listar usuarios (GET /usuarios/)
class UsuarioViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UsuarioSerializer
    pagination_class = paginador_customizado

    def get_queryset(self):
        return Usuario.objects.all()


# ViewSet CRUD completo (create, list, retrieve, update, delete)
class UsuarioCRUDView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    pagination_class = paginador_customizado
    queryset = Usuario.objects.all()


# ViewSet público que SOLO permite listar usuarios y sin autenticación
class UsuarioPublicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UsuarioSerializer
    pagination_class = paginador_customizado
    queryset = Usuario.objects.all()
    permission_classes = [AllowAny]


# ViewSet que SOLO permite listar usuarios pero requiere autenticación
class UsuarioAuthViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UsuarioSerializer
    pagination_class = paginador_customizado
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]


# ViewSet CRUD completo SOLO para administradores
class UsuarioAdminViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    pagination_class = paginador_customizado
    queryset = Usuario.objects.all()
    permission_classes = [IsAdminUser]
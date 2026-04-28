from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import VehiculoSerializer
from vehicles.models import Vehiculo
from vehicles.api.paginator import paginador_customizado


# ViewSet que solo permite listar vehículos
class VehiculoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = VehiculoSerializer
    pagination_class = paginador_customizado
    queryset = Vehiculo.objects.all()

    # permite ordenar resultados en la URL (?ordering=marca o ?ordering=anio)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['marca', 'anio']  # campos por los que se puede ordenar
    ordering = ['marca']  # orden por defecto


# CRUD completo de vehículos (create, list, retrieve, update, delete)
class VehiculoCRUDView(viewsets.ModelViewSet):
    serializer_class = VehiculoSerializer
    pagination_class = paginador_customizado
    queryset = Vehiculo.objects.all()

    # sistema de ordenación en la API
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['marca', 'anio']
    ordering = ['marca']


# Listado público de vehículos (sin autenticación)
class VehiculoPublicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = VehiculoSerializer
    pagination_class = paginador_customizado
    queryset = Vehiculo.objects.all()
    permission_classes = [AllowAny]  # cualquiera puede acceder


# Listado de vehículos solo para usuarios autenticados
class VehiculoAuthViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = VehiculoSerializer
    pagination_class = paginador_customizado
    queryset = Vehiculo.objects.all()
    permission_classes = [IsAuthenticated]  # requiere login


# CRUD completo solo para administradores
class VehiculoAdminViewSet(viewsets.ModelViewSet):
    serializer_class = VehiculoSerializer
    pagination_class = paginador_customizado
    queryset = Vehiculo.objects.all()
    permission_classes = [IsAdminUser]  # solo admin puede usarlo
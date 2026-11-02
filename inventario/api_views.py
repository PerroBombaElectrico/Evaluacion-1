from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import DetalleVenta, Producto, Venta
from .serializers import (
    DetalleVentaSerializer,
    ProductoSerializer,
    VentaSerializer,
)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = (IsAuthenticated,)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.prefetch_related("detalles__producto").all()
    serializer_class = VentaSerializer
    permission_classes = (IsAuthenticated,)


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.select_related("venta", "producto").all()
    serializer_class = DetalleVentaSerializer
    permission_classes = (IsAuthenticated,)

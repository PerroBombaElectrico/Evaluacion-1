from rest_framework import serializers

from .models import DetalleVenta, Producto, Venta


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            "id",
            "nombre",
            "descripcion",
            "categoria",
            "precio",
            "stock",
            "fecha_creacion",
            "fecha_actualizacion",
        )
        read_only_fields = ("id", "fecha_creacion", "fecha_actualizacion")


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = (
            "id",
            "venta",
            "producto",
            "cantidad",
            "precio_unitario",
            "subtotal",
        )
        read_only_fields = ("id", "precio_unitario", "subtotal")


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = (
            "id",
            "numero_venta",
            "fecha_venta",
            "total",
            "estado",
            "stock_actualizado",
            "detalles",
        )
        read_only_fields = (
            "id",
            "numero_venta",
            "total",
            "stock_actualizado",
            "detalles",
        )

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código",
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Precio",
    )
    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Stock",
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

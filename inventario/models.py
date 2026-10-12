from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    categoria = models.CharField(max_length=80, blank=True, default="General", verbose_name="Categoría")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Precio",
    )
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock disponible",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def clean(self):
        super().clean()
        if self.precio is not None and self.precio < Decimal("0.00"):
            raise ValidationError({"precio": "El precio no puede ser negativo."})
        if self.stock is not None and self.stock < 0:
            raise ValidationError({"stock": "El stock no puede ser negativo."})

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    ESTADO_CHOICES = (
        ("completada", "Completada"),
        ("anulada", "Anulada"),
    )

    numero_venta = models.CharField(max_length=30, unique=True, verbose_name="Número de venta")
    fecha_venta = models.DateTimeField(default=timezone.now, verbose_name="Fecha y hora")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), verbose_name="Total")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="completada", verbose_name="Estado")
    stock_actualizado = models.BooleanField(default=False, verbose_name="Stock actualizado")

    class Meta:
        ordering = ["-fecha_venta"]
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def generar_numero(self):
        prefijo = "VT"
        ultimo = Venta.objects.filter(numero_venta__startswith=prefijo).order_by("-id").first()
        if ultimo and ultimo.numero_venta:
            try:
                numero = int(ultimo.numero_venta.replace(prefijo, "")) + 1
            except ValueError:
                numero = 1
        else:
            numero = 1
        return f"{prefijo}{numero:06d}"

    def actualizar_total(self):
        self.total = sum((detalle.subtotal for detalle in self.detalles.all()), Decimal("0.00"))

    def save(self, *args, **kwargs):
        if not self.numero_venta:
            self.numero_venta = self.generar_numero()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_venta


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE, verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_venta", verbose_name="Producto")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), verbose_name="Subtotal")

    class Meta:
        ordering = ["id"]
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    def clean(self):
        super().clean()
        if self.cantidad is not None and self.cantidad <= 0:
            raise ValidationError({"cantidad": "La cantidad debe ser mayor que cero."})
        if self.producto and self.producto.stock < self.cantidad and self.venta_id and not self.venta.stock_actualizado:
            raise ValidationError({"cantidad": "No hay stock suficiente para este producto."})

    def save(self, *args, **kwargs):
        if self.precio_unitario is None and self.producto_id:
            self.precio_unitario = self.producto.precio
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.actualizar_total()
        self.venta.save(update_fields=["total"])

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"



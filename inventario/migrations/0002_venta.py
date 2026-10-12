from decimal import Decimal

import django.core.validators
import django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Venta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numero_venta",
                    models.CharField(max_length=30, unique=True, verbose_name="Número de venta"),
                ),
                (
                    "fecha_venta",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Fecha y hora",
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=12,
                        verbose_name="Total",
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[("completada", "Completada"), ("anulada", "Anulada")],
                        default="completada",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "stock_actualizado",
                    models.BooleanField(default=False, verbose_name="Stock actualizado"),
                ),
            ],
            options={
                "verbose_name": "Venta",
                "verbose_name_plural": "Ventas",
                "ordering": ["-fecha_venta"],
            },
        ),
        migrations.CreateModel(
            name="DetalleVenta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cantidad",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Cantidad",
                    ),
                ),
                (
                    "precio_unitario",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Precio unitario",
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=12,
                        verbose_name="Subtotal",
                    ),
                ),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="detalles_venta",
                        to="inventario.producto",
                        verbose_name="Producto",
                    ),
                ),
                (
                    "venta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="inventario.venta",
                        verbose_name="Venta",
                    ),
                ),
            ],
            options={
                "verbose_name": "Detalle de venta",
                "verbose_name_plural": "Detalles de venta",
                "ordering": ["id"],
            },
        ),
    ]

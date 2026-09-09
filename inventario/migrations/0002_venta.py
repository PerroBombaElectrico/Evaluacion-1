from decimal import Decimal

import django.core.validators
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
                    "cantidad",
                    models.PositiveIntegerField(verbose_name="Cantidad"),
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
                    "total",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Total",
                    ),
                ),
                (
                    "fecha_venta",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Fecha de venta",
                    ),
                ),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ventas",
                        to="inventario.producto",
                        verbose_name="Producto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Venta",
                "verbose_name_plural": "Ventas",
                "ordering": ["-fecha_venta"],
            },
        ),
    ]

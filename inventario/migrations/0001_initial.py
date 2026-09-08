from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Producto",
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
                    "codigo",
                    models.CharField(
                        max_length=30,
                        unique=True,
                        verbose_name="Código",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        max_length=100,
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "descripcion",
                    models.TextField(
                        blank=True,
                        verbose_name="Descripción",
                    ),
                ),
                (
                    "precio",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal("0.00")
                            )
                        ],
                        verbose_name="Precio",
                    ),
                ),
                (
                    "stock",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Stock",
                    ),
                ),
                (
                    "fecha_creacion",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Fecha de creación",
                    ),
                ),
                (
                    "fecha_actualizacion",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Fecha de actualización",
                    ),
                ),
            ],
            options={
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
                "ordering": ["nombre"],
            },
        ),
    ]

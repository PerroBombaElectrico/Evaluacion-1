from django.db import migrations


def repair_missing_sales_tables(apps, schema_editor):
    existing_tables = set(schema_editor.connection.introspection.table_names())
    producto = apps.get_model("inventario", "Producto")
    venta = apps.get_model("inventario", "Venta")
    detalle_venta = apps.get_model("inventario", "DetalleVenta")

    if venta._meta.db_table not in existing_tables:
        schema_editor.create_model(venta)

    if detalle_venta._meta.db_table not in existing_tables:
        if producto._meta.db_table not in existing_tables:
            raise RuntimeError(
                f"La tabla requerida {producto._meta.db_table!r} no existe."
            )
        schema_editor.create_model(detalle_venta)


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0003_remove_producto_codigo_producto_categoria_and_more"),
    ]

    operations = [
        migrations.RunPython(
            repair_missing_sales_tables,
            reverse_code=migrations.RunPython.noop,
        ),
    ]

from django.contrib import admin

from .models import DetalleVenta, Producto, Venta


admin.site.site_title = "Tienda Admin"
admin.site.site_header = "Tienda | Panel administrativo"
admin.site.index_title = "Gestión de la tienda"

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "fecha_creacion")
    search_fields = ("nombre", "categoria")
    list_filter = ("categoria", "fecha_creacion")
    ordering = ("nombre",)
    list_per_page = 15

admin.site.register(model_or_iterable=Producto, admin_class=ProductoAdmin)


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    fields = ("producto", "cantidad", "precio_unitario", "subtotal")
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("producto",)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("numero_venta", "fecha_venta", "total", "estado")
    search_fields = ("numero_venta",)
    list_filter = ("fecha_venta", "estado")
    ordering = ("-fecha_venta",)
    inlines = [DetalleVentaInline]
    readonly_fields = ("total",)


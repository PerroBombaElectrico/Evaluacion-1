from django.contrib import admin

from .models import DetalleVenta, Producto, Venta


admin.site.site_title = "Administración de Tienda ES02"
admin.site.site_header = "Administración de Tienda ES02"
admin.site.index_title = "Administración de Tienda ES02"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "fecha_creacion")
    search_fields = ("nombre", "categoria")
    list_filter = ("categoria", "fecha_creacion")
    ordering = ("nombre",)
    list_per_page = 15


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

from django.contrib import admin

from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "precio", "stock")
    search_fields = ("codigo", "nombre")
    list_filter = ("fecha_creacion",)
    ordering = ("nombre","stock")

admin.site.register(model_or_iterable=Producto, admin_class=ProductoAdmin)
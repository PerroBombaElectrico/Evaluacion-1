from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.producto_lista, name="producto_lista"),
    path("productos/nuevo/", views.producto_crear, name="producto_crear"),
    path("productos/<int:pk>/", views.producto_detalle, name="producto_detalle"),
    path("productos/<int:pk>/editar/", views.producto_actualizar, name="producto_actualizar"),
    path("productos/<int:pk>/eliminar/", views.producto_eliminar, name="producto_eliminar"),
    path("ventas/", views.venta_lista, name="venta_lista"),
    path("ventas/crear/", views.venta_crear, name="venta_crear"),
    path("ventas/<int:pk>/", views.venta_detalle, name="venta_detalle"),
    path("ventas/<int:pk>/editar/", views.venta_actualizar, name="venta_actualizar"),
    path("ventas/<int:pk>/eliminar/", views.venta_eliminar, name="venta_eliminar"),
    path("reportes/ventas/", views.reporte_ventas, name="reporte_ventas"),
]

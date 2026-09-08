from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.producto_lista, name="producto_lista"),
    path(
        "producto/nuevo/",
        views.producto_crear,
        name="producto_crear",
    ),
    path(
        "producto/<int:pk>/",
        views.producto_detalle,
        name="producto_detalle",
    ),
    path(
        "producto/<int:pk>/editar/",
        views.producto_actualizar,
        name="producto_actualizar",
    ),
    path(
        "producto/<int:pk>/eliminar/",
        views.producto_eliminar,
        name="producto_eliminar",
    ),
]

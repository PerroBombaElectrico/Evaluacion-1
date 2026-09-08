from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def producto_lista(request):
    productos = Producto.objects.all()
    return render(
        request,
        "inventario/producto_lista.html",
        {"productos": productos},
    )


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(
        request,
        "inventario/producto_detalle.html",
        {"producto": producto},
    )


def producto_crear(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            messages.success(
                request,
                f'El producto "{producto.nombre}" fue creado correctamente.',
            )
            return redirect("inventario:producto_detalle", pk=producto.pk)
    else:
        formulario = ProductoForm()

    return render(
        request,
        "inventario/producto_form.html",
        {
            "formulario": formulario,
            "titulo": "Crear producto",
            "boton": "Guardar producto",
        },
    )


def producto_actualizar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            producto = formulario.save()
            messages.success(
                request,
                f'El producto "{producto.nombre}" fue actualizado correctamente.',
            )
            return redirect("inventario:producto_detalle", pk=producto.pk)
    else:
        formulario = ProductoForm(instance=producto)

    return render(
        request,
        "inventario/producto_form.html",
        {
            "formulario": formulario,
            "producto": producto,
            "titulo": "Actualizar producto",
            "boton": "Actualizar producto",
        },
    )


def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(
            request,
            f'El producto "{nombre_producto}" fue eliminado correctamente.',
        )
        return redirect("inventario:producto_lista")

    return render(
        request,
        "inventario/producto_confirmar_eliminacion.html",
        {"producto": producto},
    )

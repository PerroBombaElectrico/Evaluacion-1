from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.forms import BaseFormSet, formset_factory
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm, ReporteVentasForm, VentaItemForm
from .models import DetalleVenta, Producto, Venta


def _validar_stock_formset(formset):
    cantidades_por_producto = {}
    for form in formset.forms:
        cleaned = form.cleaned_data
        if not cleaned or "producto" not in cleaned:
            continue
        producto = cleaned["producto"]
        cantidad = cleaned["cantidad"]
        cantidades_por_producto[producto.pk] = cantidades_por_producto.get(producto.pk, 0) + cantidad
        if cantidades_por_producto[producto.pk] > producto.stock:
            raise ValidationError(f"No hay suficiente stock de {producto.nombre}. Stock disponible: {producto.stock}.")


@login_required
@user_passes_test(lambda user: user.is_staff)
def producto_lista(request):
    query = request.GET.get("q", "").strip()
    productos = Producto.objects.all()
    if query:
        productos = productos.filter(nombre__icontains=query)

    paginator_obj = Paginator(productos, 10)
    page_obj = paginator_obj.get_page(request.GET.get("page"))

    return render(
        request,
        "inventario/producto_lista.html",
        {"productos": page_obj, "query": query},
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "inventario/producto_detalle.html", {"producto": producto})


@login_required
@user_passes_test(lambda user: user.is_staff)
def producto_crear(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            messages.success(request, f'El producto "{producto.nombre}" fue creado correctamente.')
            return redirect("inventario:producto_detalle", pk=producto.pk)
    else:
        formulario = ProductoForm()

    return render(
        request,
        "inventario/producto_form.html",
        {"formulario": formulario, "titulo": "Crear producto", "boton": "Guardar producto"},
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def producto_actualizar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            producto = formulario.save()
            messages.success(request, f'El producto "{producto.nombre}" fue actualizado correctamente.')
            return redirect("inventario:producto_detalle", pk=producto.pk)
    else:
        formulario = ProductoForm(instance=producto)

    return render(
        request,
        "inventario/producto_form.html",
        {"formulario": formulario, "producto": producto, "titulo": "Actualizar producto", "boton": "Actualizar producto"},
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'El producto "{nombre_producto}" fue eliminado correctamente.')
        return redirect("inventario:producto_lista")

    return render(request, "inventario/producto_confirmar_eliminacion.html", {"producto": producto})


@login_required
@user_passes_test(lambda user: user.is_staff)
def venta_lista(request):
    ventas = Venta.objects.select_related().order_by("-fecha_venta")
    from django.core.paginator import Paginator

    paginator = Paginator(ventas, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "inventario/venta_lista.html", {"ventas": page_obj})


@login_required
@user_passes_test(lambda user: user.is_staff)
def venta_detalle(request, pk):
    venta = get_object_or_404(Venta.objects.prefetch_related("detalles__producto"), pk=pk)
    return render(request, "inventario/venta_detalle.html", {"venta": venta})


@login_required
@user_passes_test(lambda user: user.is_staff)
def venta_crear(request):
    VentaFormSet = formset_factory(VentaItemForm, extra=3, min_num=1, validate_min=True)

    if request.method == "POST":
        formset = VentaFormSet(request.POST)
        if not formset.is_valid():
            error_messages = [str(error) for error in formset.non_form_errors()]
            for error in error_messages:
                messages.error(request, error)
            return render(
                request,
                "inventario/venta_form.html",
                {"formset": formset, "titulo": "Registrar venta", "error_message": " ".join(error_messages)},
            )

        try:
            with transaction.atomic():
                _validar_stock_formset(formset)
                venta = Venta.objects.create(total=Decimal("0.00"))
                for form in formset.forms:
                    cleaned = form.cleaned_data
                    if not cleaned or "producto" not in cleaned:
                        continue
                    producto = cleaned["producto"]
                    cantidad = cleaned["cantidad"]
                    precio_unitario = producto.precio
                    subtotal = Decimal(cantidad) * precio_unitario
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal,
                    )
                    producto.stock -= cantidad
                    producto.save(update_fields=["stock"])
                venta.total = sum((detalle.subtotal for detalle in venta.detalles.all()), Decimal("0.00"))
                venta.stock_actualizado = True
                venta.save(update_fields=["total", "stock_actualizado"])
                messages.success(request, f'La venta {venta.numero_venta} fue registrada correctamente.')
                return redirect("inventario:venta_detalle", pk=venta.pk)
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
    else:
        formset = VentaFormSet()

    return render(request, "inventario/venta_form.html", {"formset": formset, "titulo": "Registrar venta"})


@login_required
@user_passes_test(lambda user: user.is_staff)
def venta_actualizar(request, pk):
    venta = get_object_or_404(Venta.objects.prefetch_related("detalles__producto"), pk=pk)
    VentaFormSet = formset_factory(VentaItemForm, extra=3, min_num=1, validate_min=True)
    initial_data = [{"producto": detalle.producto, "cantidad": detalle.cantidad} for detalle in venta.detalles.all()]

    if request.method == "POST":
        formset = VentaFormSet(request.POST)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    productos_originales = {detalle.producto_id: detalle.cantidad for detalle in venta.detalles.all()}
                    cantidades_por_producto = {}
                    for form in formset.forms:
                        cleaned = form.cleaned_data
                        if not cleaned or "producto" not in cleaned:
                            continue
                        producto = cleaned["producto"]
                        cantidad = cleaned["cantidad"]
                        cantidades_por_producto[producto.pk] = cantidades_por_producto.get(producto.pk, 0) + cantidad
                        if cantidades_por_producto[producto.pk] > producto.stock + productos_originales.get(producto.pk, 0):
                            raise ValidationError(f"No hay suficiente stock de {producto.nombre}.")

                    for detalle in venta.detalles.all():
                        detalle.producto.stock += detalle.cantidad
                        detalle.producto.save(update_fields=["stock"])
                    venta.detalles.all().delete()
                    total = Decimal("0.00")
                    for form in formset.forms:
                        cleaned = form.cleaned_data
                        if not cleaned or "producto" not in cleaned:
                            continue
                        producto = cleaned["producto"]
                        cantidad = cleaned["cantidad"]
                        precio_unitario = producto.precio
                        subtotal = Decimal(cantidad) * precio_unitario
                        DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal,
                        )
                        producto.stock -= cantidad
                        producto.save(update_fields=["stock"])
                        total += subtotal
                    venta.total = total
                    venta.stock_actualizado = True
                    venta.save(update_fields=["total", "stock_actualizado"])
                    messages.success(request, f'La venta {venta.numero_venta} fue actualizada correctamente.')
                    return redirect("inventario:venta_detalle", pk=venta.pk)
            except ValidationError as exc:
                for error in exc.messages:
                    messages.error(request, error)
    else:
        formset = VentaFormSet(initial=initial_data)

    return render(request, "inventario/venta_form.html", {"formset": formset, "titulo": "Actualizar venta", "venta": venta})


@login_required
@user_passes_test(lambda user: user.is_staff)
def venta_eliminar(request, pk):
    venta = get_object_or_404(Venta.objects.prefetch_related("detalles__producto"), pk=pk)

    if request.method == "POST":
        with transaction.atomic():
            for detalle in venta.detalles.all():
                detalle.producto.stock += detalle.cantidad
                detalle.producto.save(update_fields=["stock"])
            venta.detalles.all().delete()
            venta.delete()
        messages.success(request, f'La venta {venta.numero_venta} fue eliminada correctamente.')
        return redirect("inventario:venta_lista")

    return render(request, "inventario/venta_confirmar_eliminacion.html", {"venta": venta})


@login_required
@user_passes_test(lambda user: user.is_staff)
def reporte_ventas(request):
    form = ReporteVentasForm(request.GET or None)
    ventas = []
    total_vendido = Decimal("0.00")
    numero_ventas = 0

    if form.is_valid():
        fecha_inicio = form.cleaned_data["fecha_inicio"]
        fecha_fin = form.cleaned_data["fecha_fin"]
        ventas = Venta.objects.filter(fecha_venta__date__gte=fecha_inicio, fecha_venta__date__lte=fecha_fin).order_by("-fecha_venta")
        numero_ventas = ventas.count()
        total_vendido = sum((venta.total for venta in ventas), Decimal("0.00"))

    return render(
        request,
        "inventario/reporte_ventas.html",
        {"form": form, "ventas": ventas, "total_vendido": total_vendido, "numero_ventas": numero_ventas},
    )


def inicio(request):
    productos = Producto.objects.count()
    ventas = Venta.objects.count()
    total_ventas = Venta.objects.aggregate(total=Sum("total"))
    context = {
        "total_productos": productos,
        "total_ventas": ventas,
        "total_vendido": total_ventas["total"] or Decimal("0.00"),
    }
    return render(request, "inventario/index.html", context)

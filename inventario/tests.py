from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import ProductoForm, ReporteVentasForm
from .models import DetalleVenta, Producto, Venta


class ProductoModelTests(TestCase):
    def test_precio_negativo_y_stock_negativo_invalidan_modelo(self):
        producto = Producto(nombre="Teclado", descripcion="", precio=Decimal("-1.00"), stock=-1)
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_precio_cero_y_stock_valido_son_permitidos(self):
        producto = Producto(nombre="Mouse", descripcion="", precio=Decimal("0.00"), stock=0)
        producto.full_clean()
        self.assertEqual(producto.stock, 0)


class ProductoFormTests(TestCase):
    def test_form_rechaza_precio_negativo(self):
        form = ProductoForm(
            data={
                "nombre": "Monitor",
                "descripcion": "",
                "categoria": "Tecnología",
                "precio": "-5.00",
                "stock": 6,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("precio", form.errors)

    def test_form_rechaza_stock_negativo(self):
        form = ProductoForm(
            data={
                "nombre": "Cámara",
                "descripcion": "",
                "categoria": "Tecnología",
                "precio": "150.00",
                "stock": -1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("stock", form.errors)


class VentaLogicTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Laptop",
            descripcion="Portátil",
            categoria="Tecnología",
            precio=Decimal("1500.00"),
            stock=10,
        )
        self.user = get_user_model().objects.create_user(username="admin", password="admin123", is_staff=True)

    def test_detalle_calcula_subtotal_y_venta_total(self):
        venta = Venta.objects.create(numero_venta="VT000001", total=Decimal("0.00"))
        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=self.producto.precio,
        )
        self.assertEqual(detalle.subtotal, Decimal("3000.00"))
        venta.refresh_from_db()
        self.assertEqual(venta.total, Decimal("3000.00"))

    def test_creacion_de_venta_reduce_stock_y_actualiza_total(self):
        client = self.client
        client.force_login(self.user)
        response = client.post(
            reverse("inventario:venta_crear"),
            {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "1",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-producto": str(self.producto.pk),
                "form-0-cantidad": "3",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)
        venta = Venta.objects.latest("id")
        self.assertEqual(venta.total, Decimal("4500.00"))

    def test_venta_invalid_si_no_hay_stock_suficiente(self):
        client = self.client
        client.force_login(self.user)
        response = client.post(
            reverse("inventario:venta_crear"),
            {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "1",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-producto": str(self.producto.pk),
                "form-0-cantidad": "11",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay suficiente stock de Laptop. Stock disponible: 10.")
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)

    def test_reporte_por_fecha_calcula_total_y_total_ventas(self):
        self.client.force_login(self.user)
        Venta.objects.create(numero_venta="VT000001", total=Decimal("100.00"), fecha_venta="2025-01-10T10:00:00Z")
        Venta.objects.create(numero_venta="VT000002", total=Decimal("250.00"), fecha_venta="2025-01-15T11:00:00Z")
        Venta.objects.create(numero_venta="VT000003", total=Decimal("300.00"), fecha_venta="2025-01-20T09:00:00Z")

        response = self.client.get(
            reverse("inventario:reporte_ventas"),
            {"fecha_inicio": "2025-01-10", "fecha_fin": "2025-01-15"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VT000001")
        self.assertContains(response, "VT000002")
        self.assertNotContains(response, "VT000003")
        self.assertContains(response, "350.00")
        self.assertContains(response, "2")


class AuthAndViewTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(username="staff", password="pass123", is_staff=True)
        self.normal = get_user_model().objects.create_user(username="normal", password="pass123")

    def test_producto_lista_requires_staff(self):
        response = self.client.get(reverse("inventario:producto_lista"))
        self.assertEqual(response.status_code, 302)

    def test_producto_crear_view_creates_product_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("inventario:producto_crear"),
            {
                "nombre": "Parlante",
                "descripcion": "Parlante bluetooth",
                "categoria": "Electrónica",
                "precio": "85.50",
                "stock": "12",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre="Parlante").exists())

    def test_reporte_form_rechaza_fecha_inicio_mayor_que_fin(self):
        form = ReporteVentasForm(data={"fecha_inicio": "2025-02-10", "fecha_fin": "2025-02-05"})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)


class VentaModelTests(TestCase):
    def test_numero_venta_se_generates_when_blank(self):
        venta = Venta.objects.create(total=Decimal("0.00"))
        self.assertTrue(venta.numero_venta.startswith("VT"))

from django import forms
from django.core.exceptions import ValidationError

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "categoria", "precio", "stock"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Descripción"}),
            "categoria": forms.TextInput(attrs={"class": "form-control", "placeholder": "Categoría"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00", "placeholder": "0.00"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": "0", "placeholder": "0"}),
        }
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock disponible",
        }

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is not None and precio < 0:
            raise ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return stock


class VentaItemForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1", "placeholder": "Cantidad"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producto"].queryset = Producto.objects.order_by("nombre")

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")
        if producto and cantidad is not None and producto.stock < cantidad:
            raise ValidationError(f"No hay suficiente stock de {producto.nombre}. Stock disponible: {producto.stock}.")
        return cleaned_data


class ReporteVentasForm(forms.Form):
    fecha_inicio = forms.DateField(
        label="Fecha inicial",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    fecha_fin = forms.DateField(
        label="Fecha final",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise ValidationError("La fecha inicial no puede ser posterior a la fecha final.")
        return cleaned_data

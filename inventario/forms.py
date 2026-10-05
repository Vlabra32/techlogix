from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "precio",
            "stock",
            "sku",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del producto",
            }),
            "categoria": forms.Select(attrs={
                "class": "form-control",
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
            }),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "SKU del producto",
            }),
        }

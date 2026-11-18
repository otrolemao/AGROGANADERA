from django import forms

from .models import Ternero


class TerneroForm(forms.ModelForm):
    """Formulario de alta/edicion de terneros con widgets de Bootstrap 5."""

    class Meta:
        model = Ternero
        fields = [
            'numero_identificador',
            'peso_kg',
            'fecha_nacimiento',
            'disponible_venta',
            'precio_estimado',
            'raza',
        ]
        widgets = {
            'numero_identificador': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ARETE-011',
                'maxlength': 50,
            }),
            'peso_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ej: 120.50',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'disponible_venta': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'precio_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ej: 450000',
            }),
            'raza': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def clean_peso_kg(self):
        peso = self.cleaned_data.get('peso_kg')
        if peso is not None and peso <= 0:
            raise forms.ValidationError('El peso debe ser mayor que cero.')
        return peso

    def clean_precio_estimado(self):
        precio = self.cleaned_data.get('precio_estimado')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

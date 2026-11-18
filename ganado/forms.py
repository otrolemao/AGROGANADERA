from django import forms
from django.core.exceptions import ValidationError

from .formatos import formatear_clp
from .models import Ternero


class PrecioCLPField(forms.IntegerField):
    """Entero que acepta puntos de miles opcionales: '450.000' o '450000'."""

    default_error_messages = {
        'invalid': (
            'Ingresa un precio válido en pesos. Usa solo números y puntos de '
            'miles, por ejemplo 450.000.'
        ),
    }

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, str):
            limpio = (
                value.strip()
                .replace('$', '')
                .replace(' ', '')
                .replace('\xa0', '')
                .replace('.', '')
            )
            if not limpio:
                return None
            if not limpio.isdigit():
                raise ValidationError(
                    self.error_messages['invalid'], code='invalid'
                )
            value = limpio
        return super().to_python(value)


class TerneroForm(forms.ModelForm):
    """Formulario de alta/edicion de terneros con widgets de Bootstrap 5."""

    precio_estimado = PrecioCLPField(
        label='Precio Estimado ($)',
        min_value=0,
        help_text=(
            'Puedes escribir con o sin puntos de miles '
            '(por ejemplo: 450.000 o 450000).'
        ),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'numeric',
            'placeholder': 'Ej: 450.000',
            'autocomplete': 'off',
        }),
    )

    peso_kg = forms.DecimalField(
        label='Peso (kg)',
        max_digits=6,
        decimal_places=2,
        localize=True,
        help_text='Puedes usar coma o punto decimal (por ejemplo: 120,50).',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'decimal',
            'placeholder': 'Ej: 120,50',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Al editar, muestra el precio con puntos de miles.
        if not self.is_bound and self.instance and self.instance.pk:
            precio = self.instance.precio_estimado
            if precio is not None:
                self.initial['precio_estimado'] = formatear_clp(precio)

    class Meta:
        model = Ternero
        fields = [
            'numero_identificador',
            'peso_kg',
            'fecha_nacimiento',
            'disponible_venta',
            'precio_estimado',
            'raza',
            'imagen',
        ]
        widgets = {
            'numero_identificador': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ARETE-011',
                'maxlength': 50,
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'disponible_venta': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'raza': forms.Select(attrs={
                'class': 'form-select',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
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

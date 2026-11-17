from django import forms
from .models import Ternero

class TerneroForm(forms.ModelForm):
    class Meta:
        model = Ternero
        fields = ['numero_identificador', 'peso_kg', 'fecha_nacimiento', 'disponible_venta', 'precio_estimado', 'raza']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
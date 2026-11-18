"""Filtros de plantilla para mostrar montos en pesos chilenos (CLP)."""

from django import template

from ganado.formatos import formatear_clp

register = template.Library()


@register.filter(name='clp')
def clp(valor):
    """Formatea un monto con puntos de miles: 450000 -> 450.000."""
    return formatear_clp(valor)

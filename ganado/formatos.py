"""Utilidades de formato propias del proyecto AgroGanadera."""


def formatear_clp(valor):
    """Devuelve un monto entero con puntos de miles (formato CLP).

    Ejemplos: 450000 -> '450.000'; 1234567 -> '1.234.567'.
    Si el valor no es convertible a entero se devuelve tal cual.
    """
    if valor in (None, ''):
        return ''
    try:
        monto = int(valor)
    except (TypeError, ValueError):
        return valor
    return f'{monto:,}'.replace(',', '.')

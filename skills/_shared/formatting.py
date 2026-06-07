"""Formato de números y montos en convención argentina."""


def format_ars(value, simbolo="$ "):
    """Formatea un monto como `$ 1.234,56` (punto de miles, coma decimal).

    >>> format_ars(1234.5)
    '$ 1.234,50'
    >>> format_ars(-17690.61)
    '$ -17.690,61'
    >>> format_ars(0)
    '$ 0,00'
    """
    try:
        n = float(value)
    except (TypeError, ValueError):
        return f"{simbolo}0,00"
    entero = f"{abs(n):,.2f}"          # 1,234.56  (estilo inglés)
    entero = entero.replace(",", "X").replace(".", ",").replace("X", ".")
    signo = "-" if n < 0 else ""
    return f"{simbolo}{signo}{entero}"


def format_pct(value, decimales=0):
    """Formatea un porcentaje, ej. 21 -> '21%'."""
    try:
        return f"{float(value):.{decimales}f}%"
    except (TypeError, ValueError):
        return "0%"

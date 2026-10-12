from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import template


register = template.Library()


@register.filter
def pesos_chilenos(value):
    """Muestra un monto como pesos chilenos sin decimales."""
    try:
        monto = Decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        return value

    signo = "-" if monto < 0 else ""
    entero = f"{abs(monto):.0f}"
    grupos = []
    while entero:
        grupos.insert(0, entero[-3:])
        entero = entero[:-3]
    return f"{signo}$ {'.'.join(grupos)}"

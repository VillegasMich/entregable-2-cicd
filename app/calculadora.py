"""Operaciones aritméticas básicas utilizadas por la aplicación."""

AUTORES = """mvillegas6@eafit.edu.co,
            epatinov@eafit.edu.co,
            mvasquezb@eafit.edu.co"""


def sumar(a, b):
    """Devuelve la suma de ``a`` y ``b``."""
    return a + b


def restar(a, b):
    """Devuelve la resta de ``a`` menos ``b``."""
    return a - b


def multiplicar(a, b):
    """Devuelve el producto de ``a`` y ``b``."""
    return a * b


def dividir(a, b):
    """Devuelve la división de ``a`` entre ``b``; lanza ``ZeroDivisionError``
    si ``b`` es 0."""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b

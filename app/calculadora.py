# app/calculadora.py

AUTORES = "mvillegas6@eafit.edu.co, epatinov@eafit.edu.co, mvasquezb@eafit.edu.co"


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b

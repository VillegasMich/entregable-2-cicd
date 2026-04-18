"""Aplicación Flask que expone una calculadora web simple."""
from flask import Flask, render_template, request
from .calculadora import sumar, restar, multiplicar, dividir

app = Flask(__name__)


OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
}


@app.route("/", methods=["GET"])
def index():
    """Renderiza el formulario vacío de la calculadora."""
    return render_template("index.html", resultado=None)


@app.route("/", methods=["POST"])
def calcular():
    """Calcula el resultado de la operación enviada mediante el formulario."""
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operacion = request.form["operacion"]

        operador = OPERACIONES.get(operacion)
        if operador is None:
            resultado = "Operación no válida"
        else:
            resultado = operador(num1, num2)
    except ValueError:
        resultado = "Error: Introduce números válidos"
    except ZeroDivisionError:
        resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=False, port=5000, host="0.0.0.0")  # Quita debug=True para producción

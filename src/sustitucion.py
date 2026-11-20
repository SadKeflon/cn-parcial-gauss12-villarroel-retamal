"""Sustitución regresiva, con instrumentación opcional."""

from math import isfinite


def sustitucion_regresiva(U, b_transformado, contador=None):
    """Resuelve Ux=b sin utilizar rutinas de álgebra lineal externas."""
    n = len(U)
    if n == 0 or len(b_transformado) != n or any(len(fila) != n for fila in U):
        raise ValueError("U debe ser cuadrada y b debe tener el mismo número de filas")

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        pivote = float(U[i][i])
        if pivote == 0.0:
            raise ZeroDivisionError(f"Pivote cero en la fila {i + 1}")
        suma = 0.0
        for j in range(i + 1, n):
            suma += float(U[i][j]) * x[j]
            if contador is not None:
                contador.producto_sustitucion()
                contador.suma_sustitucion()

        x[i] = (float(b_transformado[i]) - suma) / pivote
        if contador is not None:
            contador.suma_sustitucion()
            contador.producto_sustitucion()
        if not isfinite(x[i]):
            raise ArithmeticError(f"Resultado no finito en la fila {i + 1}")
    return x

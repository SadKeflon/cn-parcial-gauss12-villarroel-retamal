
"""Sustitución regresiva para sistemas triangulares superiores."""

from math import isfinite


def sustitucion_regresiva(U, b_transformado):
    """Resuelve Ux = b mediante sustitución regresiva."""

    n = len(U)

    # Verificamos que las dimensiones del sistema sean correctas.
    if n == 0 or len(b_transformado) != n or any(len(fila) != n for fila in U):
        raise ValueError(
            "U debe ser cuadrada y b debe tener el mismo número de filas"
        )

    # Inicializamos el vector solución.
    x = [0.0] * n

    # Recorremos desde la última ecuación hasta la primera.
    for i in range(n - 1, -1, -1):

        pivote = float(U[i][i])

        if pivote == 0.0:
            raise ZeroDivisionError(
                f"Pivote cero en la fila {i + 1}"
            )

        # Sumamos los términos cuyas incógnitas ya conocemos.
        suma = 0.0

        for j in range(i + 1, n):
            suma += float(U[i][j]) * x[j]

        # Despejamos la incógnita correspondiente.
        x[i] = (float(b_transformado[i]) - suma) / pivote

        if not isfinite(x[i]):
            raise ArithmeticError(
                f"Resultado no finito en la fila {i + 1}"
            )

    return x

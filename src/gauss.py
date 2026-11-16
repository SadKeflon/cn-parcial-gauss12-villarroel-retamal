
"""Eliminación gaussiana sin pivoteo (solo triangularización).

La sustitución regresiva y el pivoteo se implementarán en otros avances.
"""


def triangularizar_sin_pivoteo(A, b):
    """Devuelve U, b_transformado y L con los multiplicadores.

    Trabaja en float64 (float de Python) y no modifica los datos recibidos.
    No utiliza funciones de resolución de bibliotecas externas.
    """
    n = len(A)

    if n == 0 or any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError(
            "El sistema debe ser cuadrado y tener un valor de b por fila"
        )

    # Copias de los datos para no modificar las matrices originales.
    U = [[float(valor) for valor in fila] for fila in A]
    b_transformado = [float(valor) for valor in b]

    # Matriz L: diagonal de unos y ceros en las demás posiciones.
    L = [
        [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]

    # En una matriz de 12x12 realizamos 11 pasos de eliminación.
    for k in range(n - 1):

        pivote = U[k][k]

        if pivote == 0.0:
            raise ZeroDivisionError(
                f"Pivote cero en el paso {k + 1}; se requiere pivoteo"
            )

        # Eliminamos los valores que están debajo del pivote.
        for i in range(k + 1, n):

            # Calculamos el multiplicador solamente una vez.
            multiplicador = U[i][k] / pivote
            L[i][k] = multiplicador

            # El elemento debajo de la diagonal queda anulado.
            U[i][k] = 0.0

            # Actualizamos solamente las columnas necesarias.
            for j in range(k + 1, n):
                U[i][j] -= multiplicador * U[k][j]

            # Aplicamos la misma operación al vector b.
            b_transformado[i] -= multiplicador * b_transformado[k]

    # Comprobamos el último pivote.
    if U[n - 1][n - 1] == 0.0:
        raise ZeroDivisionError(
            "Pivote cero en la última fila; no hay solución única"
        )

    return U, b_transformado, L

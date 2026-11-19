
"""Eliminación gaussiana con pivoteo parcial escalado."""


def triangularizar_pivoteo_escalado(A, b):
    """Triangulariza Ax=b mediante pivoteo parcial escalado.

    Devuelve U, b_transformado, L, permutacion e intercambios.
    La permutacion registra el orden de las filas originales.
    """

    n = len(A)

    if n == 0 or any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError(
            "El sistema debe ser cuadrado y tener un valor de b por fila"
        )

    # Copiamos los datos para conservar los originales.
    U = [[float(valor) for valor in fila] for fila in A]
    b_transformado = [float(valor) for valor in b]

    # L guardará los multiplicadores de la eliminación.
    L = [
        [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]

    # Factor de escala: máximo valor absoluto de cada fila.
    escalas = [
        max(abs(valor) for valor in fila)
        for fila in U
    ]

    # Identificamos el orden original de las filas.
    permutacion = list(range(n))
    intercambios = 0

    if any(escala == 0.0 for escala in escalas):
        raise ZeroDivisionError("La matriz tiene una fila nula")

    # Eliminamos las columnas debajo de la diagonal.
    for k in range(n - 1):

        # Buscamos la fila con el mayor cociente escalado.
        fila_pivote = max(
            range(k, n),
            key=lambda i: abs(U[i][k]) / escalas[i]
        )

        if U[fila_pivote][k] == 0.0:
            raise ZeroDivisionError(
                f"Pivote cero en el paso {k + 1}"
            )

        # Si encontramos un mejor pivote, intercambiamos filas.
        if fila_pivote != k:

            U[k], U[fila_pivote] = U[fila_pivote], U[k]

            b_transformado[k], b_transformado[fila_pivote] = (
                b_transformado[fila_pivote],
                b_transformado[k]
            )

            # La escala pertenece a su fila original.
            escalas[k], escalas[fila_pivote] = (
                escalas[fila_pivote],
                escalas[k]
            )

            permutacion[k], permutacion[fila_pivote] = (
                permutacion[fila_pivote],
                permutacion[k]
            )

            # Conservamos correctamente los multiplicadores
            # almacenados en las columnas anteriores de L.
            for j in range(k):
                L[k][j], L[fila_pivote][j] = (
                    L[fila_pivote][j],
                    L[k][j]
                )

            intercambios += 1

        # A partir de aquí eliminamos como en Gauss.
        pivote = U[k][k]

        for i in range(k + 1, n):

            multiplicador = U[i][k] / pivote
            L[i][k] = multiplicador

            U[i][k] = 0.0

            for j in range(k + 1, n):
                U[i][j] -= multiplicador * U[k][j]

            b_transformado[i] -= multiplicador * b_transformado[k]

    if U[n - 1][n - 1] == 0.0:
        raise ZeroDivisionError("Pivote cero en la última fila")

    return U, b_transformado, L, permutacion, intercambios

"""Eliminación gaussiana sin pivoteo, con instrumentación opcional."""


def triangularizar_sin_pivoteo(A, b, contador=None):
    """Entrega U, vector transformado y L sin alterar los datos originales."""
    n = len(A)
    if n == 0 or any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError("El sistema debe ser cuadrado y tener un valor de b por fila")

    U = [[float(valor) for valor in fila] for fila in A]
    b_transformado = [float(valor) for valor in b]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    if contador is not None:
        contador.iniciar(U)

    for k in range(n - 1):
        pivote = U[k][k]
        if pivote == 0.0:
            raise ZeroDivisionError(f"Pivote cero en el paso {k + 1}; se requiere pivoteo")
        if contador is not None:
            contador.abrir_paso(k)

        for i in range(k + 1, n):
            multiplicador = U[i][k] / pivote
            L[i][k] = multiplicador
            if contador is not None:
                contador.multiplicacion_division(k)
                contador.multiplicador(multiplicador)

            U[i][k] = 0.0
            for j in range(k + 1, n):
                U[i][j] -= multiplicador * U[k][j]
                if contador is not None:
                    contador.multiplicacion_division(k)
                    contador.suma_resta(k)
            b_transformado[i] -= multiplicador * b_transformado[k]
            if contador is not None:
                contador.multiplicacion_division(k)
                contador.suma_resta(k)

        if contador is not None:
            contador.cerrar_paso(k, U, pivote, k)

    if U[n - 1][n - 1] == 0.0:
        raise ZeroDivisionError("Pivote cero en la última fila; no hay solución única")
    return U, b_transformado, L

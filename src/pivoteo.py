"""Eliminación gaussiana con pivoteo parcial escalado y conteo opcional."""


def triangularizar_pivoteo_escalado(A, b, contador=None):
    """Entrega U, vector transformado, L, permutación e intercambios."""
    n = len(A)
    if n == 0 or any(len(fila) != n for fila in A) or len(b) != n:
        raise ValueError("El sistema debe ser cuadrado y tener un valor de b por fila")

    U = [[float(valor) for valor in fila] for fila in A]
    b_transformado = [float(valor) for valor in b]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    escalas = [max(abs(valor) for valor in fila) for fila in U]
    permutacion = list(range(n))
    intercambios = 0

    if any(escala == 0.0 for escala in escalas):
        raise ZeroDivisionError("La matriz tiene una fila nula")

    if contador is not None:
        contador.iniciar(U)
        contador.costo_escalas(n)

    for k in range(n - 1):
        if contador is not None:
            contador.abrir_paso(k)
            contador.costo_busqueda(k, n - k)

        fila_pivote = max(range(k, n), key=lambda i: abs(U[i][k]) / escalas[i])
        if U[fila_pivote][k] == 0.0:
            raise ZeroDivisionError(f"Pivote cero en el paso {k + 1}")

        if fila_pivote != k:
            U[k], U[fila_pivote] = U[fila_pivote], U[k]
            b_transformado[k], b_transformado[fila_pivote] = (
                b_transformado[fila_pivote], b_transformado[k]
            )
            escalas[k], escalas[fila_pivote] = escalas[fila_pivote], escalas[k]
            permutacion[k], permutacion[fila_pivote] = (
                permutacion[fila_pivote], permutacion[k]
            )
            for j in range(k):
                L[k][j], L[fila_pivote][j] = L[fila_pivote][j], L[k][j]
            intercambios += 1
            if contador is not None:
                contador.intercambio()

        pivote = U[k][k]
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
            contador.cerrar_paso(k, U, pivote, permutacion[k])

    if U[n - 1][n - 1] == 0.0:
        raise ZeroDivisionError("Pivote cero en la última fila")
    return U, b_transformado, L, permutacion, intercambios

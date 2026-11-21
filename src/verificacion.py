"""Residuo en precisión extendida y controles independientes de biblioteca.

Ningún control de biblioteca se utiliza para producir la solución principal.
"""

from decimal import Decimal, localcontext


def residuo_decimal(A, b, x, precision=80):
    """Calcula r=b-Ax con productos y acumulaciones en Decimal.

    Los datos A y b deben proceder de cargar_sistema, sin redondeo previo.
    Decimal.from_float representa exactamente cada x guardado en float64.
    """
    n = len(A)
    if n == 0 or len(b) != n or len(x) != n or any(len(fila) != n for fila in A):
        raise ValueError("Dimensiones incompatibles para calcular el residuo")
    if precision < 30:
        raise ValueError("Utilizar al menos 30 cifras de precisión decimal")

    resultado = []
    with localcontext() as contexto:
        contexto.prec = precision
        for i in range(n):
            suma = Decimal(0)
            for j in range(n):
                suma += Decimal(str(A[i][j])) * Decimal.from_float(float(x[j]))
            resultado.append(Decimal(str(b[i])) - suma)
    return resultado


def norma_infinito(vector):
    """Devuelve máximo absoluto de un vector Decimal (o numérico)."""
    if not vector:
        raise ValueError("El vector no puede estar vacío")
    return max(abs(valor) for valor in vector)


def control_numpy(A, b):
    """Solución externa solo como contraste, NO como algoritmo entregado."""
    import numpy as np

    matriz = np.array([[float(v) for v in fila] for fila in A], dtype=float)
    vector = np.array([float(v) for v in b], dtype=float)
    return np.linalg.solve(matriz, vector).tolist()


def control_mpmath(A, b, precision=100):
    """Referencia de control independiente de alta precisión, nunca solución principal.

    Se utiliza como referencia independiente de alta precisión para evaluar
    el error y estimar los dígitos significativos defendibles.
    """
    import mpmath as mp

    with mp.workdps(precision):
        matriz = mp.matrix([[mp.mpf(str(v)) for v in fila] for fila in A])
        vector = mp.matrix([mp.mpf(str(v)) for v in b])
        solucion = mp.lu_solve(matriz, vector)
        return [mp.nstr(v, precision - 10) for v in solucion]

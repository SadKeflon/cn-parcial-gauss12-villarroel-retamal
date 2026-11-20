"""Una corrección iterativa reutilizando los factores L y U existentes."""

from math import isfinite

from src.sustitucion import sustitucion_regresiva
from src.verificacion import norma_infinito, residuo_decimal


def correccion_desde_factores(L, U, residuo, permutacion=None):
    """Resuelve L U delta = P*r SIN volver a factorizar A."""
    n = len(L)
    if n == 0 or len(U) != n or len(residuo) != n:
        raise ValueError("Factores y residuo incompatibles")
    if permutacion is None:
        permutacion = list(range(n))
    if sorted(permutacion) != list(range(n)):
        raise ValueError("Permutación inválida")

    r_ordenado = [float(residuo[permutacion[i]]) for i in range(n)]

    # Sustitución hacia adelante en L y = P*r; L tiene diagonal 1.
    y = [0.0] * n
    for i in range(n):
        y[i] = r_ordenado[i] - sum(float(L[i][j]) * y[j] for j in range(i))
    return sustitucion_regresiva(U, y)


def refinar_una_vez(A, b, x, L, U, permutacion=None, precision=80):
    """Una pasada x_nuevo=x+delta usando un residuo Decimal de alta precisión.

    Retorna (solucion_nueva, informacion). Puede no mejorar si está mal
    condicionado: esa eventualidad se muestra, no se oculta.
    """
    residuo_antes = residuo_decimal(A, b, x, precision)
    delta = correccion_desde_factores(L, U, residuo_antes, permutacion)
    nueva = [float(x[i]) + delta[i] for i in range(len(x))]
    if not all(isfinite(valor) for valor in nueva):
        raise ArithmeticError("El refinamiento produjo valores no finitos")
    residuo_despues = residuo_decimal(A, b, nueva, precision)
    antes = norma_infinito(residuo_antes)
    despues = norma_infinito(residuo_despues)
    return nueva, {
        "residuo_antes": antes,
        "residuo_despues": despues,
        "mejoro": despues < antes,
        "norma_correccion": max(abs(v) for v in delta),
    }

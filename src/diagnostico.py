"""Métricas de condición, error relativo y mantisa; no resuelve Ax=b."""

from decimal import Decimal, localcontext
from math import floor, isfinite, log10, log2
from sys import float_info


def estimar_condicion_2(A):
    """Usa numpy.linalg.cond solo para estimar κ2, no para resolver Ax=b."""
    import numpy as np

    matriz = np.asarray([[float(v) for v in fila] for fila in A], dtype=float)
    return float(np.linalg.cond(matriz, p=2))


def cota_condicion(A):
    condicion = estimar_condicion_2(A)
    return condicion, condicion * float_info.epsilon


def error_relativo_infinito(x, referencia):
    """Compara contra la referencia de control extendido, con 80 cifras."""
    if len(x) != len(referencia) or not x:
        raise ValueError("Soluciones incompatibles")
    with localcontext() as contexto:
        contexto.prec = 80
        ref = [Decimal(str(valor)) for valor in referencia]
        estimacion = [Decimal.from_float(float(valor)) for valor in x]
        numerador = max(abs(a - b) for a, b in zip(estimacion, ref))
        denominador = max(abs(valor) for valor in ref)
        return float(numerador / denominador) if denominador else float(numerador)


def digitos_defendibles(valor, referencia, maximo=16):
    """Cifras garantizables según el error relativo frente al control.

    Criterio conservador: |error relativo| < 0.5 * 10**(-d).
    Para referencia cero utiliza error absoluto, que debe identificarse.
    """
    with localcontext() as contexto:
        contexto.prec = 90
        real = Decimal(str(referencia))
        aproximacion = Decimal.from_float(float(valor))
        error = abs(aproximacion - real)
        relativo = error / abs(real) if real else error
    if relativo == 0:
        return maximo
    numero = float(relativo)
    if not isfinite(numero) or numero <= 0:
        return 0
    return max(0, min(maximo, floor(-log10(2 * numero))))


def bits_amplificacion_estimada(maximo_multiplicador, crecimiento):
    """Indicador heurístico: NO equivale a bits perdidos medidos exactamente."""
    escala = max(1.0, maximo_multiplicador, crecimiento)
    return max(0.0, log2(escala))

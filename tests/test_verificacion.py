"""Comprobaciones del residuo extendido y controles independientes."""

from decimal import Decimal

import pytest

from src.cargar_datos import cargar_sistema
from src.gauss import triangularizar_sin_pivoteo
from src.sustitucion import sustitucion_regresiva
from src.verificacion import (
    control_mpmath, control_numpy, norma_infinito, residuo_decimal,
)


def test_residuo_decimal_solucion_exacta():
    A = [[Decimal("2"), Decimal("1")], [Decimal("1"), Decimal("3")]]
    b = [Decimal("4"), Decimal("7")]
    r = residuo_decimal(A, b, [1.0, 2.0])
    assert r == [Decimal(0), Decimal(0)]
    assert norma_infinito(r) == 0


def test_residuo_refleja_error_inyectado():
    A = [[Decimal("1")]]
    b = [Decimal("1.001")]
    r = residuo_decimal(A, b, [1.0])
    assert norma_infinito(r) == Decimal("0.001")


def test_control_numpy_y_mpmath_coinciden_sistema_simple():
    A = [[Decimal("2"), Decimal("1")], [Decimal("1"), Decimal("3")]]
    b = [Decimal("4"), Decimal("7")]
    assert control_numpy(A, b) == pytest.approx([1, 2])
    assert [float(t) for t in control_mpmath(A, b)] == pytest.approx([1, 2])


def test_sistema_real_entrega_residuo_finito():
    A, b = cargar_sistema()
    U, bt, _ = triangularizar_sin_pivoteo(A, b)
    x = sustitucion_regresiva(U, bt)
    r = residuo_decimal(A, b, x)
    assert len(r) == 12
    assert norma_infinito(r).is_finite()

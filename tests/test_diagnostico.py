"""Pruebas de condición y comparación con control de precisión extendida."""

import pytest

from src.cargar_datos import cargar_sistema
from src.diagnostico import (
    bits_amplificacion_estimada, cota_condicion, digitos_defendibles,
    error_relativo_infinito,
)


def test_digitos_con_error_conocido():
    assert digitos_defendibles(1.0, "1") == 16
    assert 5 <= digitos_defendibles(1.0000001, "1") <= 7
    assert digitos_defendibles(2.0, "1") == 0


def test_error_relativo_exactamente_cero():
    assert error_relativo_infinito([1.0, -2.0], ["1", "-2"]) == 0


def test_bits_amplificacion():
    assert bits_amplificacion_estimada(1024, 2) == pytest.approx(10)


def test_condicion_sistema_12x12_grande():
    A, _ = cargar_sistema()
    condicion, cota = cota_condicion(A)
    assert condicion > 1e10
    assert cota > 0

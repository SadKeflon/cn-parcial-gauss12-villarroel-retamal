"""El contador se incrementa donde ocurre cada operación elemental."""

import pytest

from src.cargar_datos import cargar_sistema
from src.conteo import ContadorOperaciones
from src.gauss import triangularizar_sin_pivoteo
from src.pivoteo import triangularizar_pivoteo_escalado
from src.sustitucion import sustitucion_regresiva


def test_conteo_matriz_2x2():
    A, b = [[2, 1], [4, 3]], [5, 11]
    c = ContadorOperaciones("sin pivoteo")
    U, bt, L = triangularizar_sin_pivoteo(A, b, c)
    x = sustitucion_regresiva(U, bt, c)
    assert x == pytest.approx([2, 1])
    assert c.mult_div_eliminacion == 3  # 1 división, 2 multiplicaciones
    assert c.sum_rest_eliminacion == 2
    assert c.flops_sustitucion == 6
    assert c.flops_aritmeticos == 11
    assert len(c.pasos) == 1


def test_conteo_sistema_12x12_sin_pivote():
    A, b = cargar_sistema()
    c = ContadorOperaciones("sin pivoteo")
    U, bt, _ = triangularizar_sin_pivoteo(A, b, c)
    sustitucion_regresiva(U, bt, c)
    assert len(c.pasos) == 11
    assert c.mult_div_eliminacion == 638
    assert c.sum_rest_eliminacion == 572
    assert c.flops_sustitucion == 156
    assert c.flops_aritmeticos == 1366
    assert c.factor_crecimiento >= 1
    assert c.multiplicador_maximo > 1


def test_sobrecosto_pivoteo_escalado():
    A, b = cargar_sistema()
    c = ContadorOperaciones("pivoteo escalado")
    U, bt, _, _, intercambios = triangularizar_pivoteo_escalado(A, b, c)
    sustitucion_regresiva(U, bt, c)
    assert c.flops_aritmeticos == 1366
    assert c.divisiones_busqueda == 77
    assert c.comparaciones_busqueda == 66
    assert c.comparaciones_escalas == 132
    assert c.intercambios == intercambios
    assert c.flops_totales_con_pivote == 1443
    assert len(c.traza) == 11


def test_la_instrumentacion_no_cambia_solucion():
    A, b = [[3, 1], [1, 2]], [7, 5]
    U1, b1, _ = triangularizar_sin_pivoteo(A, b)
    c = ContadorOperaciones("control")
    U2, b2, _ = triangularizar_sin_pivoteo(A, b, c)
    assert U1 == U2
    assert b1 == b2
    assert sustitucion_regresiva(U1, b1) == pytest.approx(
        sustitucion_regresiva(U2, b2, c)
    )

"""La corrección usa la factorización previa y no vuelve a eliminar."""

import pytest

from src.cargar_datos import cargar_sistema
from src.pivoteo import triangularizar_pivoteo_escalado
from src.refinamiento import correccion_desde_factores, refinar_una_vez
from src.sustitucion import sustitucion_regresiva


def test_correccion_desde_lu_simple():
    A = [[2, 1], [1, 3]]
    b = [4, 7]
    U, bt, L, p, _ = triangularizar_pivoteo_escalado(A, b)
    delta = correccion_desde_factores(L, U, [4, 7], p)
    assert delta == pytest.approx([1, 2])


def test_refinamiento_corrige_solucion_perturbada():
    A = [[2, 1], [1, 3]]
    b = [4, 7]
    U, bt, L, p, _ = triangularizar_pivoteo_escalado(A, b)
    nueva, info = refinar_una_vez(A, b, [1.1, 1.9], L, U, p)
    assert nueva == pytest.approx([1, 2])
    assert info["mejoro"]
    assert info["residuo_despues"] < info["residuo_antes"]


def test_refinamiento_real_completa_una_pasada():
    A, b = cargar_sistema()
    U, bt, L, p, _ = triangularizar_pivoteo_escalado(A, b)
    x = sustitucion_regresiva(U, bt)
    nueva, info = refinar_una_vez(A, b, x, L, U, p)
    assert len(nueva) == 12
    assert info["residuo_antes"].is_finite()
    assert info["residuo_despues"].is_finite()
    assert info["norma_correccion"] >= 0

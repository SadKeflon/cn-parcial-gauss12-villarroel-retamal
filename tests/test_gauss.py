
"""Pruebas del primer avance de eliminación gaussiana."""

import pytest

from src.cargar_datos import cargar_sistema
from src.gauss import triangularizar_sin_pivoteo


def test_triangulariza_un_sistema_pequeno():
    A = [
        [2, 1, 1],
        [4, 3, 2],
        [6, 5, 5]
    ]
    b = [5, 10, 19]

    U, b_final, L = triangularizar_sin_pivoteo(A, b)

    assert U[0] == pytest.approx([2, 1, 1])
    assert U[1] == pytest.approx([0, 1, 0])
    assert U[2] == pytest.approx([0, 0, 2])

    assert b_final == pytest.approx([5, 0, 4])

    assert L[1][0] == pytest.approx(2)
    assert L[2][0] == pytest.approx(3)
    assert L[2][1] == pytest.approx(2)


def test_l_por_u_reproduce_la_matriz_inicial():
    A = [
        [2, 1, 1],
        [4, 3, 2],
        [6, 5, 5]
    ]

    U, _, L = triangularizar_sin_pivoteo(A, [5, 10, 19])
    n = len(A)

    producto = [
        [
            sum(L[i][k] * U[k][j] for k in range(n))
            for j in range(n)
        ]
        for i in range(n)
    ]

    for original, recuperada in zip(A, producto):
        assert recuperada == pytest.approx(original)


def test_no_modifica_los_datos_de_entrada():
    A = [[2, 1], [4, 3]]
    b = [5, 10]

    A_original = [fila.copy() for fila in A]
    b_original = b.copy()

    triangularizar_sin_pivoteo(A, b)

    assert A == A_original
    assert b == b_original


def test_rechaza_pivote_inicial_cero():
    A = [
        [0, 2, 1],
        [1, -1, 3],
        [2, 1, -1]
    ]
    b = [5, 6, 1]

    with pytest.raises(ZeroDivisionError, match="Pivote cero"):
        triangularizar_sin_pivoteo(A, b)


def test_triangulariza_los_12_datos_del_enunciado():
    A, b = cargar_sistema()

    U, b_final, L = triangularizar_sin_pivoteo(A, b)

    assert len(U) == len(b_final) == len(L) == 12

    assert all(
        U[i][j] == 0.0
        for i in range(12)
        for j in range(i)
    )

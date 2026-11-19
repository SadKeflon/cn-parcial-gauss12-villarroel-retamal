
"""Pruebas para la sustitución regresiva."""

import pytest

from src.cargar_datos import cargar_sistema
from src.gauss import triangularizar_sin_pivoteo
from src.sustitucion import sustitucion_regresiva


def test_sistema_triangular_2x2():
    U = [
        [3, 1],
        [0, 2]
    ]
    b = [5, 4]

    x = sustitucion_regresiva(U, b)

    assert x == pytest.approx([1, 2])


def test_integracion_con_eliminacion_gaussiana():
    A = [
        [2, 1, 1],
        [4, 3, 2],
        [6, 5, 5]
    ]
    b = [5, 10, 19]

    U, b_final, L = triangularizar_sin_pivoteo(A, b)
    x = sustitucion_regresiva(U, b_final)

    assert x == pytest.approx([1.5, 0, 2])


def test_rechaza_dimensiones_incorrectas():
    U = [
        [2, 1],
        [0, 3]
    ]
    b = [5]

    with pytest.raises(ValueError, match="cuadrada"):
        sustitucion_regresiva(U, b)


def test_detecta_pivote_cero():
    U = [
        [2, 1],
        [0, 0]
    ]
    b = [5, 3]

    with pytest.raises(ZeroDivisionError, match="Pivote cero"):
        sustitucion_regresiva(U, b)


def test_solucion_del_sistema_12x12():
    A, b = cargar_sistema()

    # Primero triangularizamos utilizando el método del commit 4.
    U, b_final, L = triangularizar_sin_pivoteo(A, b)

    # Después aplicamos sustitución regresiva.
    x = sustitucion_regresiva(U, b_final)

    assert len(x) == 12

    # Verificamos el residuo respecto al sistema original.
    A_float = [[float(valor) for valor in fila] for fila in A]
    b_float = [float(valor) for valor in b]

    residuos = [
        b_float[i] - sum(
            A_float[i][j] * x[j] for j in range(12)
        )
        for i in range(12)
    ]

    residuo_maximo = max(abs(valor) for valor in residuos)
    escala = max(1.0, max(abs(valor) for valor in b_float))

    assert residuo_maximo / escala < 1e-10


"""Pruebas del pivoteo parcial escalado."""

import pytest

from src.cargar_datos import cargar_sistema
from src.pivoteo import triangularizar_pivoteo_escalado
from src.sustitucion import sustitucion_regresiva


def verificar_factorizacion(A, b, L, U, b_final, permutacion):
    """Comprueba las igualdades PA=LU y Pb=L*b_final."""
    n = len(A)

    for i in range(n):
        for j in range(n):
            reconstruido = sum(
                L[i][k] * U[k][j]
                for k in range(n)
            )

            assert reconstruido == pytest.approx(
                float(A[permutacion[i]][j])
            )

        transformado = sum(
            L[i][k] * b_final[k]
            for k in range(n)
        )

        assert transformado == pytest.approx(
            float(b[permutacion[i]])
        )


def test_escala_elige_fila_distinta_del_mayor_absoluto():
    A = [[5, 1000], [4, 1]]
    b = [2005, 6]

    U, b_final, L, permutacion, intercambios = (
        triangularizar_pivoteo_escalado(A, b)
    )

    # El mayor absoluto es 5, pero el mejor
    # pivote escalado es 4.
    assert permutacion == [1, 0]
    assert intercambios == 1
    assert U[0] == pytest.approx([4, 1])

    x = sustitucion_regresiva(U, b_final)

    assert x == pytest.approx([1, 2])

    verificar_factorizacion(A, b, L, U, b_final, permutacion)


def test_intercambia_multiplicadores_guardados_en_l():
    A = [
        [2, 0, 1],
        [3, 1, 1],
        [1, 2, 0]
    ]
    b = [5, 8, 5]

    U, b_final, L, permutacion, intercambios = (
        triangularizar_pivoteo_escalado(A, b)
    )

    # El intercambio ocurre en la segunda columna.
    assert permutacion == [0, 2, 1]
    assert intercambios == 1

    assert L[1][0] == pytest.approx(0.5)
    assert L[2][0] == pytest.approx(1.5)

    x = sustitucion_regresiva(U, b_final)

    assert x == pytest.approx([1, 2, 3])

    verificar_factorizacion(A, b, L, U, b_final, permutacion)


def test_no_modifica_los_datos_originales():
    A = [[0, 2], [3, 1]]
    b = [4, 5]

    copia_A = [fila.copy() for fila in A]
    copia_b = b.copy()

    triangularizar_pivoteo_escalado(A, b)

    assert A == copia_A
    assert b == copia_b


def test_rechaza_matriz_singular():
    A = [[1, 2], [2, 4]]
    b = [3, 6]

    with pytest.raises(ZeroDivisionError, match="Pivote cero"):
        triangularizar_pivoteo_escalado(A, b)


def test_sistema_12x12():
    A, b = cargar_sistema()

    U, b_final, L, permutacion, intercambios = (
        triangularizar_pivoteo_escalado(A, b)
    )

    x = sustitucion_regresiva(U, b_final)

    assert len(x) == 12
    assert sorted(permutacion) == list(range(12))
    assert intercambios >= 1

    # Debe quedar una matriz triangular superior.
    assert all(
        U[i][j] == 0.0
        for i in range(12)
        for j in range(i)
    )

    verificar_factorizacion(
        A, b, L, U, b_final, permutacion
    )

    # Comprobación inicial del residuo en float64.
    residuos = [
        float(b[i]) - sum(
            float(A[i][j]) * x[j]
            for j in range(12)
        )
        for i in range(12)
    ]

    escala = max(
        1.0,
        max(abs(float(valor)) for valor in b)
    )

    assert max(abs(valor) for valor in residuos) / escala < 1e-10

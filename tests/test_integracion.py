"""Pruebas de extremo a extremo antes de producir resultados de entrega."""

from src.cargar_datos import cargar_sistema
from src.conteo import ContadorOperaciones
from src.consistencia import verificar_factorizacion, verificar_triangular_superior
from src.gauss import triangularizar_sin_pivoteo
from src.pivoteo import triangularizar_pivoteo_escalado
from src.refinamiento import refinar_una_vez
from src.sustitucion import sustitucion_regresiva
from src.verificacion import norma_infinito, residuo_decimal


def test_sistema_real_ambos_metodos():
    A, b = cargar_sistema()
    for metodo in ("sin", "escalado"):
        contador = ContadorOperaciones(metodo)
        if metodo == "sin":
            U, bt, L = triangularizar_sin_pivoteo(A, b, contador)
            p = list(range(12))
        else:
            U, bt, L, p, _ = triangularizar_pivoteo_escalado(A, b, contador)
        x = sustitucion_regresiva(U, bt, contador)
        r = residuo_decimal(A, b, x)
        assert verificar_triangular_superior(U)
        assert verificar_factorizacion(A, L, U, p) < 1e-11
        assert contador.flops_aritmeticos == 1366
        assert contador.factor_crecimiento >= 1
        assert norma_infinito(r).is_finite()
        _, info = refinar_una_vez(A, b, x, L, U, p)
        assert info["residuo_despues"].is_finite()


def test_sistema_pequeno_detecta_factorizacion_mala():
    A = [[2, 1], [4, 3]]
    U, _, L = triangularizar_sin_pivoteo(A, [5, 11])
    assert verificar_factorizacion(A, L, U) < 1e-14
    L[1][0] += 1
    assert verificar_factorizacion(A, L, U) > 0.1

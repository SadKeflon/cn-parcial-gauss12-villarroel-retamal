"""Verificación estructural de la eliminación y de PA=LU."""


def verificar_factorizacion(A, L, U, permutacion=None):
    """Devuelve el error máximo normalizado en PA-LU.

    No ejecuta ninguna nueva factorización.
    """
    n = len(A)
    if n == 0 or len(L) != n or len(U) != n:
        raise ValueError("Dimensiones incompatibles")
    if permutacion is None:
        permutacion = list(range(n))
    if sorted(permutacion) != list(range(n)):
        raise ValueError("Permutación inválida")

    escala = max(1.0, max(abs(float(v)) for fila in A for v in fila))
    error_max = 0.0
    for i in range(n):
        for j in range(n):
            elemento = sum(float(L[i][k]) * float(U[k][j]) for k in range(n))
            error_max = max(error_max, abs(float(A[permutacion[i]][j]) - elemento))
    return error_max / escala


def verificar_triangular_superior(U):
    n = len(U)
    return bool(n) and all(len(fila) == n for fila in U) and all(
        U[i][j] == 0.0 for i in range(n) for j in range(i)
    )

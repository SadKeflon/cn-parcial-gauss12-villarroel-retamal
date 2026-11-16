import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


# Carpeta principal del proyecto, independiente de dónde se ejecute Python.
carpeta_proyecto = Path(__file__).resolve().parent.parent


def leer_csv(ruta):
    """Lee un CSV y conserva sus cifras convirtiendo cada dato a Decimal."""
    filas = []

    with open(ruta, encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        for numero_fila, fila in enumerate(lector, start=1):
            if not fila:
                raise ValueError(f"Fila vacía en {ruta}, línea {numero_fila}")

            try:
                valores = [Decimal(valor.strip()) for valor in fila]
            except InvalidOperation as error:
                raise ValueError(
                    f"Número inválido en {ruta}, línea {numero_fila}"
                ) from error

            if not all(valor.is_finite() for valor in valores):
                raise ValueError(f"Dato no finito en {ruta}, línea {numero_fila}")

            filas.append(valores)

    return filas


def cargar_sistema(carpeta_datos=None):
    """Devuelve A (12x12) y b (12 valores) sin recortar cifras decimales."""
    if carpeta_datos is None:
        carpeta_datos = carpeta_proyecto / "datos"

    carpeta_datos = Path(carpeta_datos)
    matriz = leer_csv(carpeta_datos / "matriz_a.csv")
    filas_vector = leer_csv(carpeta_datos / "vector_b.csv")

    if len(matriz) != 12 or any(len(fila) != 12 for fila in matriz):
        raise ValueError("La matriz A debe tener exactamente 12 filas y 12 columnas")
    if len(filas_vector) != 12 or any(len(fila) != 1 for fila in filas_vector):
        raise ValueError("El vector b debe tener exactamente 12 valores, uno por fila")

    vector = [fila[0] for fila in filas_vector]
    return matriz, vector


if __name__ == "__main__":
    A, b = cargar_sistema()
    print(f"Datos validados: matriz {len(A)}x{len(A[0])}; vector de {len(b)} valores")

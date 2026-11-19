"""Pruebas básicas de lectura de los CSV entregados por el profesor."""

from decimal import Decimal

import pytest

from src.cargar_datos import cargar_sistema, leer_csv


def test_dimensiones_del_sistema():
    A, b = cargar_sistema()
    assert len(A) == 12
    assert all(len(fila) == 12 for fila in A)
    assert len(b) == 12


def test_lectura_conserva_las_cifras_originales():
    A, b = cargar_sistema()
    assert A[0][0] == Decimal("1.3407e-08")
    assert b[0] == Decimal("-0.00009885876325151139315")
    assert b[1] == Decimal("-1528.38292550107502")


def test_rechaza_matriz_con_dimensiones_incorrectas(tmp_path):
    (tmp_path / "matriz_a.csv").write_text("1,2\n3,4\n", encoding="utf-8")
    (tmp_path / "vector_b.csv").write_text("1\n2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="12 filas y 12 columnas"):
        cargar_sistema(tmp_path)


def test_rechaza_datos_no_numericos(tmp_path):
    archivo = tmp_path / "datos_invalidos.csv"
    archivo.write_text("1.5,abc\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Número inválido"):
        leer_csv(archivo)

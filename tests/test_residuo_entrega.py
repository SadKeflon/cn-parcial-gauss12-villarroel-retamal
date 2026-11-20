"""Comprueba que el archivo de entrega incluye r completo y su norma infinito."""

from decimal import Decimal
from pathlib import Path
import re

from src.main import ejecutar


def test_residuo_txt_contiene_vectores_y_normas():
    ejecutar()
    raiz = Path(__file__).resolve().parent.parent
    contenido = (raiz / "resultados" / "residuo.txt").read_text(encoding="utf-8")
    bloques = contenido.split("MÉTODO: ")[1:]
    assert len(bloques) == 2

    for bloque in bloques:
        inicial = [Decimal(x) for x in re.findall(r"^r_inicial\[\d+\] = (\S+)$", bloque, re.M)]
        final = [Decimal(x) for x in re.findall(r"^r_final\[\d+\] = (\S+)$", bloque, re.M)]
        assert len(inicial) == len(final) == 12

        norma_inicial = Decimal(re.search(r"^\|\|residuo inicial\|\|_inf: (\S+)$", bloque, re.M).group(1))
        norma_final = Decimal(re.search(r"^\|\|residuo final\|\|_inf: (\S+)$", bloque, re.M).group(1))

        assert max(abs(x) for x in inicial) == norma_inicial
        assert max(abs(x) for x in final) == norma_final

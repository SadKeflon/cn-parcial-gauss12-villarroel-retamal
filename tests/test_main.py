"""Reproducibilidad de la entrega: el comando debe regenerar resultados/."""

import csv
import subprocess
import sys
from pathlib import Path


def test_comando_main_recrea_los_resultados():
    raiz = Path(__file__).resolve().parent.parent
    proceso = subprocess.run(
        [sys.executable, "src/main.py"],
        cwd=raiz, capture_output=True, text=True, check=True,
    )
    assert "Resultados regenerados" in proceso.stdout
    carpeta = raiz / "resultados"
    for nombre in (
        "solucion.csv", "traza_eliminacion.txt",
        "conteo_flops.md", "residuo.txt", "diagnostico.json",
    ):
        assert (carpeta / nombre).is_file()
        assert (carpeta / nombre).stat().st_size > 0
    with open(carpeta / "solucion.csv", encoding="utf-8") as archivo:
        assert len(list(csv.DictReader(archivo))) == 12
    assert "| 11 |" in (carpeta / "conteo_flops.md").read_text(encoding="utf-8")

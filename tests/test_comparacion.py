
"""Pruebas del informe comparativo."""

import json
import subprocess
import sys
from pathlib import Path

from src.comparacion import generar_comparacion


RAIZ = Path(__file__).resolve().parent.parent


def test_comparacion_usa_resultados_reales():
    ruta = RAIZ / "resultados" / "diagnostico.json"

    with open(ruta, encoding="utf-8") as archivo:
        resumen = json.load(archivo)

    informe = generar_comparacion(resumen)

    assert "Sin pivoteo" in informe
    assert "Pivoteo escalado" in informe
    assert "Factor de crecimiento" in informe
    assert "Residuo inicial" in informe
    assert "Residuo final" in informe
    assert "Interpretación" in informe


def test_main_regenera_informe_comparativo():
    subprocess.run(
        [sys.executable, "src/main.py"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        check=True
    )

    ruta = RAIZ / "resultados" / "comparacion_metodos.md"

    assert ruta.is_file()

    contenido = ruta.read_text(encoding="utf-8")

    assert "Comparación de los métodos" in contenido
    assert "Flops aritméticos base" in contenido
    assert "Consideraciones" in contenido

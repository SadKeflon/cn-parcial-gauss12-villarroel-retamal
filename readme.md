# Laboratorio 3 — Eliminación gaussiana y pivoteo parcial escalado

Resuelve el sistema denso 12×12 del enunciado de Computación Numérica y compara costo operacional, pivoteo, mantisa y residuo.

**Autores:** Kevin Andrés Villarroel Duarte y Rodrigo Alonso Retamal Parada. **Asignatura:** INF-321, Universidad Católica del Maule.

## Requisitos

Python 3.10 o superior.

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python src/main.py
python -m pytest -q
```

El primer comando **reproduce automáticamente** los archivos `resultados/solucion.csv`, `resultados/traza_eliminacion.txt`, `resultados/conteo_flops.md`, `resultados/residuo.txt`, `resultados/diagnostico.json` y `resultados/comparacion_metodos.md`.

## Estructura

- `datos/`: 144 coeficientes de A y 12 valores de b, sin redondear.
- `src/`: algoritmos de Gauss, pivoteo, sustitución, conteo y verificación.
- `tests/`: pruebas de funciones y reproducción integral.
- `resultados/`: tablas, trazas y comparación de métodos regenerables con `python src/main.py`.
- `informe.md`: análisis técnico y justificación numérica.

## Resultado resumido

Solución calculada por **pivoteo parcial escalado con una pasada de refinamiento**, mostrada aquí hasta 10 cifras significativas cuando corresponda:

| Variable | Valor |
|---|---:|
| x1 | 7.384915627e-01 |
| x2 | -1.205937417e+00 |
| x3 | 4.387195200e-03 |
| x4 | -9.172645380e-02 |
| x5 | 2.846109372e+00 |
| x6 | -6.281540900e-03 |
| x7 | 1.473820592e+00 |
| x8 | -3.849271640e-02 |
| x9 | 9.152648037e-01 |
| x10 | -2.607139485e+00 |
| x11 | 5.187362940e-02 |
| x12 | -1.084937162e+00 |

- **Flops aritméticos base:** 1366 (incluye eliminación y sustitución; no incluye verificación/refinamiento).
- **Sobrecosto de divisiones para pivoteo escalado:** 77; total aritmético de la corrida: 1443.
- **Norma infinito del residuo final, Decimal 80 cifras:** `2.603187369605071005196350598E-10`.

Ver análisis completo en [informe.md](informe.md).

**Uso académico:** material destinado a la evaluación INF-321; respetar autorías y citar los recursos utilizados.

# Informe técnico — Laboratorio 3: el pivote

## Identificación

**Estudiantes:** Kevin Andrés Villarroel Duarte y Rodrigo Alonso Retamal Parada.  
**Asignatura:** Computación Numérica, INF-321, Universidad Católica del Maule.  
**Fecha:** 19 de noviembre de 2026.  
**Repositorio:** https://github.com/SadKeflon/cn-parcial-gauss12-villarroel-retamal

## Planteamiento

Se resuelve el sistema denso Ax=b, con A de tamaño 12×12 y 144 elementos no nulos. Se utilizaron íntegros los coeficientes de `datos/matriz_a.csv` y las 12 entradas decimales de `datos/vector_b.csv`, tomados de la sección 3 del enunciado del profesor. El archivo de lectura usa `Decimal` para no truncar esos datos. Las operaciones de eliminación usan float64 IEEE 754, y el residuo se evalúa independientemente con 80 cifras decimales.

El reto numérico combina filas en escalas de aproximadamente 10⁻⁵ y 10⁵, un pivote inicial de 1.3407×10⁻⁸ y una fila 7 casi dependiente de las filas 3 y 5 (según el enunciado). Una magnitud de entrada pequeña no implica necesariamente una solución pequeña: la resta entre términos de escala dispar amplifica el redondeo.

## Estrategia de eliminación

Se implementaron dos corridas: sin pivoteo y con pivoteo parcial escalado. Ambas recorren k=1,...,11; en cada paso calculan una sola vez m(i,k)=U[i,k]/U[k,k] y reutilizan ese valor para actualizar los coeficientes restantes de la fila y el elemento b[i]. Cada entrada subdiagonal se establece en cero y no se recalcula después. La matriz L almacena multiplicadores; el método escalado guarda también permutaciones, de forma que PA=LU.

El pivote escalado maximiza |U[i,k]|/s[i], con s[i]=max_j |A[i,j]|, y conserva la escala al intercambiar filas. Los multiplicadores anteriores de L deben permutarse en las columnas previas para mantener PA=LU. En ningún momento se calcula la inversa de A. Una vez obtenidos L,U se reutilizan para la corrección iterativa, sin factorizar nuevamente.

## Conteo de operaciones

El contador se actualiza **dentro del código en cada operación realmente ejecutada**. Se cuenta una flop por división, multiplicación, suma o resta; la asignación de un cero no cuenta. Los intercambios, valores absolutos y comparaciones se muestran por separado. Los costes de cálculo de residuos, verificación extendida y refinamiento se excluyen del coste mínimo de la primera resolución y se informan como trabajos de verificación adicionales.

**Tabla por paso de eliminación** (idéntico número de operaciones de actualización para las dos estrategias):

| Paso | Mul/div | Sumas/restas | Flops |
|---:|---:|---:|---:|
| 1 | 143 | 132 | 275 |
| 2 | 120 | 110 | 230 |
| 3 | 99 | 90 | 189 |
| 4 | 80 | 72 | 152 |
| 5 | 63 | 56 | 119 |
| 6 | 48 | 42 | 90 |
| 7 | 35 | 30 | 65 |
| 8 | 24 | 20 | 44 |
| 9 | 15 | 12 | 27 |
| 10 | 8 | 6 | 14 |
| 11 | 3 | 2 | 5 |

En los 11 pasos hay 638 multiplicaciones/divisiones y 572 sumas/restas: **1210 flops de eliminación**. La sustitución regresiva añade 78 multiplicaciones/divisiones y 78 sumas/restas: **156 flops**. Total instrumentado sin pivote: **1366 flops**. El pivoteo escalado añade **77 divisiones** para evaluar los cocientes de los candidatos: **1443 operaciones aritméticas** en la primera resolución, más **66 comparaciones de búsqueda**, **132 comparaciones para escala** y **8 intercambios de filas**.

Respecto a la referencia aproximada de 1486 del enunciado, 1366 difiere en −8,08 %, dentro del margen exigido de ±10 %. El informe separa la convención exacta y el sobrecosto propio del pivoteo; véase el desglose paso a paso reproducido en `resultados/conteo_flops.md`.

## Análisis de mantisa y pivoteo

| Indicador | Sin pivoteo | Pivoteo escalado |
|---|---:|---:|
| Multiplicador máximo | 2.75259e+13 | 2.46556e+09 |
| Crecimiento máximo de la matriz | 2.641224e+03 | 1.783202e+00 |
| Error relativo máximo **antes de refinar**, contra control extendido | 2.080208e-10 | 2.356518e-13 |
| Error relativo después de una pasada | 6.015950e-17 | 6.015950e-17 |

El pivote a(1,1)=1.3407×10⁻⁸ es inaceptable en comparación con coeficientes de otras filas en la primera columna. Sin intercambio se genera un multiplicador del orden de 10¹³, lo cual compromete potencialmente log₂(2.75×10¹³)≈44,65 bits por amplificación en operaciones susceptibles a cancelación. Con pivoteo escalado el máximo multiplicador global cae a ~2.47×10⁹ (estimación heurística de ~31,20 bits potencialmente afectados), y sobre todo el crecimiento de coeficientes baja de ~2641 a ~1,78. **Estas cifras en bits son indicadores de riesgo, no una medición literal de bits exactos perdidos**. La calidad se contrasta cuantitativamente con el error y el residuo.

Los errores relativos observados en esta ejecución son mejores que algunas cifras orientativas anticipadas en el texto del profesor; por eso se reportan los valores medidos y no se presentan las referencias como resultados experimentales. La comparación consolidada está en `resultados/comparacion_metodos.md`. El factor de crecimiento sin pivoteo fue aproximadamente 1,481 × 10³ veces (unas 1481 veces) el del pivoteo escalado. Asimismo, el residuo inicial sin pivoteo fue aproximadamente 1,185 × 10³ veces (unas 1185 veces) mayor.

## Condicionamiento

`numpy.linalg.cond(A,2)` estima κ₂(A)≈**3.08474375e+13**. En doble precisión ε≈2.22044605×10⁻¹⁶, de modo que κ₂(A) ε≈**6.84950707e-03**. Esta cota de peor caso no garantiza muchos dígitos correctos, pero no predice necesariamente el error de la corrida concreta: la estructura del sistema y el residuo importan. En efecto, los controles independientes ofrecen un error relativo muy inferior a la cota en esta instancia. La casi dependencia de la fila 7 (señalada en el enunciado) explica buena parte del alto κ₂.

## Resultados

Se muestran las 12 incógnitas de la solución final por pivoteo escalado, con una pasada de refinamiento elegida por reducción del residuo. El número de cifras defendibles se estimó comparando contra un **control independiente** de alta precisión (`mpmath.lu_solve` a 100 cifras), sin utilizar ese control como solucionador principal. El criterio es conservador: error relativo menor que 0,5·10⁻ᵈ. Los ceros finales se muestran en notación científica para no ocultar cifras reclamadas.

| Variable | Valor reportado | Cifras significativas defendibles |
|---|---:|---:|
| x1 | `7.38491562700000e-01` | 15 |
| x2 | `-1.20593741680000e+00` | 15 |
| x3 | `4.387195200000000e-03` | 16 |
| x4 | `-9.172645380000000e-02` | 16 |
| x5 | `2.846109372500000e+00` | 16 |
| x6 | `-6.281540900000000e-03` | 16 |
| x7 | `1.473820591600000e+00` | 16 |
| x8 | `-3.849271640000000e-02` | 16 |
| x9 | `9.152648037000000e-01` | 16 |
| x10 | `-2.60713948520000e+00` | 15 |
| x11 | `5.18736294000000e-02` | 15 |
| x12 | `-1.08493716250000e+00` | 15 |

Para cada variable, el valor `float64` sin redondear y el valor presentado se encuentran en `resultados/solucion.csv`.

## Verificación

El residuo r=b−Ax se calcula sumando productos con `Decimal` y precisión de 80 cifras, usando la representación exacta del `float64` calculado para x y los decimales originales de A,b. Para pivoteo escalado, **||r inicial||∞=6.036461860180701982869777567E-10**, y tras una pasada de refinamiento **||r||∞=2.603187369605071005196350598E-10**. Para el método sin pivoteo, los valores respectivos son **7.154579002098625744160642626E-7** y **2.603187369605071005196350598E-10**. El refinamiento resuelve L U δ=P r mediante sustituciones, reutilizando la factorización inicial.

La comprobación externa usa `numpy.linalg.solve` como control float64 y `mpmath.lu_solve` a 100 cifras solo para una referencia independiente de precisión; **ninguna de esas soluciones se usa para calcular la solución principal**. La traza de 11 pasos por método está en `resultados/traza_eliminacion.txt`. También se comprueba el error normalizado de PA−LU y la presencia de exactamente 66 ceros subdiagonales.

## Conclusiones

El pivoteo parcial escalado es la elección defendible: su sobrecosto de búsqueda es pequeño frente a la reducción del crecimiento y del error inicial. El mínimo de flops no es un criterio suficiente sin estabilidad. El refinamiento iterativo mejora la precisión sin factorizar de nuevo, aunque en un caso general debe verificarse si efectivamente mejora el residuo.

Si n=1000, el costo cúbico dominaría aún más: mantendríamos una sola factorización reutilizable, datos en memoria de forma eficiente y una biblioteca numérica optimizada si las reglas de la tarea lo permiten, sin calcular la inversa. Evaluaríamos estrategias de pivoteo, escalamiento y estimación de condicionamiento.

## Reproducibilidad

Requisitos: Python ≥3.10, NumPy ≥2.0 y <3, mpmath ≥1.3 y pytest ≥8 (véase `requirements.txt`). Ejecutar desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python src/main.py
```

El último comando recrea los seis archivos de `resultados/`, incluido `comparacion_metodos.md`. Para comprobar la reproducibilidad, primero se deben instalar las dependencias y ejecutar las pruebas desde la raíz del repositorio.

**Entorno de validación de Kevin (Windows):** Python **3.13.16**, NumPy **2.5.5**, mpmath **1.4.1** y pytest **9.2.0**. Sobre la versión de `main` que contiene las cuatro fusiones, Kevin ejecutó `python -m pytest -q` y obtuvo **39 pruebas aprobadas**.

La ejecución directa de `python src/main.py` permite generar de nuevo los archivos de `resultados/`. Su regeneración debe comprobarse al preparar la entrega final, junto con `git status`, para detectar cualquier diferencia en los archivos generados. No se atribuyen estas versiones del entorno a Rodrigo sin verificarlas en su equipo.

**Declaración de asistentes de IA:** se utilizó apoyo de asistentes de IA para estructurar el trabajo, proponer implementaciones y pruebas, revisar cambios en GitHub, preparar archivos por commit y redactar borradores del README y del informe. La ejecución local, la revisión académica y la defensa de cada línea son responsabilidad de Kevin y Rodrigo. Ambos integrantes deben revisar esta declaración, precisar cualquier uso adicional de IA y asegurarse de que describe fielmente su proceso real.

**Fuentes:** enunciado oficial «El pivote: Eliminación gaussiana con mínimo costo operacional y máxima exactitud de mantisa» (incluido en el paquete de traspaso), documentación estándar de Python (`decimal`, `csv`, `math`), NumPy y mpmath. Incorporar otras referencias consultadas durante la implementación, si corresponde.

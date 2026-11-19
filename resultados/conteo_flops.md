# Conteo instrumentado de operaciones

Convención: una flop por cada suma, resta, multiplicación o división
ejecutada. Asignaciones, valores absolutos, comparaciones e intercambios
no son flops; se informan estos últimos por separado.
El coste del vector b se incluye en eliminación; la sustitución regresiva
se cuenta aparte. No se vuelve a factorizar durante refinamiento.

## sin_pivoteo

| Paso | Multiplicaciones/divisiones | Sumas/restas | Total | Pivote | Fila original |
|---:|---:|---:|---:|---:|---:|
| 1 | 143 | 132 | 275 | 1.34070000e-08 | 1 |
| 2 | 120 | 110 | 230 | -2.53577175e+07 | 2 |
| 3 | 99 | 90 | 189 | 3.54644630e-02 | 3 |
| 4 | 80 | 72 | 152 | 8.72698985e+02 | 4 |
| 5 | 63 | 56 | 119 | -4.48908633e-05 | 5 |
| 6 | 48 | 42 | 90 | 3.74834768e+07 | 6 |
| 7 | 35 | 30 | 65 | -1.02707276e-04 | 7 |
| 8 | 24 | 20 | 44 | -8.41392245e+04 | 8 |
| 9 | 15 | 12 | 27 | -6.48013735e-04 | 9 |
| 10 | 8 | 6 | 14 | -3.82085492e+03 | 10 |
| 11 | 3 | 2 | 5 | -1.56749422e-02 | 11 |

- Eliminación: 1210 flops (638 mul/div, 572 suma/resta)
- Sustitución regresiva: 156 flops (78 mul/div, 78 suma/resta)
- **Total aritmético base: 1366 flops**
- Divisiones adicionales para seleccionar pivote: 0
- Total con esas divisiones: 1366 flops
- Comparaciones de búsqueda: 0
- Comparaciones para obtener escalas: 0
- Intercambios de filas: 0

## pivoteo_escalado

| Paso | Multiplicaciones/divisiones | Sumas/restas | Total | Pivote | Fila original |
|---:|---:|---:|---:|---:|---:|
| 1 | 143 | 132 | 275 | -8.29580538e+04 | 8 |
| 2 | 120 | 110 | 230 | 9.64576977e+04 | 2 |
| 3 | 99 | 90 | 189 | 8.82241528e-05 | 1 |
| 4 | 80 | 72 | 152 | 1.64309255e+06 | 6 |
| 5 | 63 | 56 | 119 | 1.05996914e-04 | 9 |
| 6 | 48 | 42 | 90 | 1.81683636e-02 | 11 |
| 7 | 35 | 30 | 65 | 1.01990841e+05 | 12 |
| 8 | 24 | 20 | 44 | 5.83762325e-05 | 5 |
| 9 | 15 | 12 | 27 | 1.69240670e+04 | 4 |
| 10 | 8 | 6 | 14 | -4.65815325e+03 | 10 |
| 11 | 3 | 2 | 5 | 8.29350052e-03 | 3 |

- Eliminación: 1210 flops (638 mul/div, 572 suma/resta)
- Sustitución regresiva: 156 flops (78 mul/div, 78 suma/resta)
- **Total aritmético base: 1366 flops**
- Divisiones adicionales para seleccionar pivote: 77
- Total con esas divisiones: 1443 flops
- Comparaciones de búsqueda: 66
- Comparaciones para obtener escalas: 132
- Intercambios de filas: 8

Cota de referencia del enunciado: ≈1486 flops. Nuestra convención da
1366 flops aritméticos base: diferencia de −8.08 %, dentro de ±10 %.
Para pivoteo escalado se incluyen además 77 divisiones de selección.
La referencia del enunciado redondea el coste teórico y utiliza una
convención que debe distinguirse del conteo instrumentado aquí.

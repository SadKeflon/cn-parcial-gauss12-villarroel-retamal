# Comparación de los métodos de eliminación gaussiana

Se utiliza el sistema original de 12 ecuaciones.

| Indicador | Sin pivoteo | Pivoteo escalado |
|---|---:|---:|
| Flops aritméticos base | 1366 | 1366 |
| Divisiones adicionales de pivoteo | 0 | 77 |
| Comparaciones de búsqueda | 0 | 66 |
| Comparaciones para escalas | 0 | 132 |
| Intercambios de filas | 0 | 8 |
| Multiplicador máximo | 2.753E+13 | 2.466E+9 |
| Factor de crecimiento | 2.641E+3 | 1.783E+0 |
| Residuo inicial | 7.155E-7 | 6.036E-10 |
| Residuo final | 2.603E-10 | 2.603E-10 |
| Error relativo inicial | 2.080E-10 | 2.357E-13 |
| Error relativo final | 6.016E-17 | 6.016E-17 |

## Interpretación de los resultados

- Sin pivoteo se realizaron 1366 flops aritméticos base.
- Con pivoteo escalado se realizaron 1366 flops base y 77 divisiones adicionales para seleccionar pivotes.
- El método escalado realizó 8 intercambios de filas.
- La estimación de condición es 3.085E+13.
- El factor de crecimiento sin pivoteo fue 1.481E+3 veces el del pivoteo escalado.
- Antes del refinamiento, el residuo sin pivoteo fue 1.185E+3 veces mayor que el residuo con pivoteo escalado.

## Consideraciones

- Las comparaciones y los intercambios se informan por separado de las flops.
- Los residuos finales corresponden a las soluciones seleccionadas después del refinamiento.
- Un residuo pequeño no garantiza por sí solo una solución precisa cuando la matriz está mal condicionada.
- NumPy y mpmath se usan solamente como controles independientes.

Informe generado automáticamente con `python src/main.py`.

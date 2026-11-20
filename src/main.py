"""Ejecuta los dos métodos y recrea resultados/ desde datos originales.

Comando obligatorio desde la raíz: python src/main.py
"""

import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

# Permite ejecutar el script como 'python src/main.py' sin instalar el paquete.
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.comparacion import generar_comparacion  # noqa: E402
from src.cargar_datos import cargar_sistema  # noqa: E402
from src.conteo import ContadorOperaciones  # noqa: E402
from src.consistencia import verificar_factorizacion, verificar_triangular_superior  # noqa: E402
from src.diagnostico import (  # noqa: E402
    bits_amplificacion_estimada, cota_condicion,
    digitos_defendibles, error_relativo_infinito,
)
from src.gauss import triangularizar_sin_pivoteo  # noqa: E402
from src.pivoteo import triangularizar_pivoteo_escalado  # noqa: E402
from src.refinamiento import refinar_una_vez  # noqa: E402
from src.sustitucion import sustitucion_regresiva  # noqa: E402
from src.verificacion import (  # noqa: E402
    control_mpmath, control_numpy, norma_infinito, residuo_decimal,
)


RESULTADOS = RAIZ / "resultados"


def realizar_corrida(A, b, metodo):
    contador = ContadorOperaciones(metodo)
    if metodo == "sin_pivoteo":
        U, bt, L = triangularizar_sin_pivoteo(A, b, contador)
        permutacion = list(range(len(A)))
        intercambios = 0
    elif metodo == "pivoteo_escalado":
        U, bt, L, permutacion, intercambios = triangularizar_pivoteo_escalado(
            A, b, contador
        )
    else:
        raise ValueError(f"Método desconocido: {metodo}")

    x = sustitucion_regresiva(U, bt, contador)
    r_antes = residuo_decimal(A, b, x)
    x_refinado, info = refinar_una_vez(A, b, x, L, U, permutacion)

    # La decisión usa el residuo calculado independientemente, no el control
    # de biblioteca. Si el refinamiento no mejora, conservamos el original.
    usar_refinamiento = info["mejoro"]
    x_final = x_refinado if usar_refinamiento else x
    r_final = residuo_decimal(A, b, x_final)

    if not verificar_triangular_superior(U):
        raise ArithmeticError("Falló la triangularización")
    error_factorizacion = verificar_factorizacion(A, L, U, permutacion)
    if error_factorizacion > 1e-10:
        raise ArithmeticError("La factorización PA=LU no es consistente")

    return {
        "metodo": metodo,
        "contador": contador,
        "x": x,
        "x_refinado": x_refinado,
        "x_final": x_final,
        "refinamiento_aplicado": usar_refinamiento,
        "residuo_antes": norma_infinito(r_antes),
        "vector_residuo_inicial": r_antes,
        "residuo_refinado": info["residuo_despues"],
        "residuo_final": norma_infinito(r_final),
        "vector_residuo_final": r_final,
        "correccion_maxima": info["norma_correccion"],
        "error_factorizacion": error_factorizacion,
        "intercambios": intercambios,
        "permutacion": permutacion,
    }


def generar_conteo(corridas):
    salida = [
        "# Conteo instrumentado de operaciones",
        "",
        "Convención: una flop por cada suma, resta, multiplicación o división",
        "ejecutada. Asignaciones, valores absolutos, comparaciones e intercambios",
        "no son flops; se informan estos últimos por separado.",
        "El coste del vector b se incluye en eliminación; la sustitución regresiva",
        "se cuenta aparte. No se vuelve a factorizar durante refinamiento.",
        "",
    ]
    for corrida in corridas:
        c = corrida["contador"]
        salida += [
            f"## {corrida['metodo']}", "",
            "| Paso | Multiplicaciones/divisiones | Sumas/restas | Total | Pivote | Fila original |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
        for p in c.pasos:
            md = p["multiplicaciones_divisiones"]
            sr = p["sumas_restas"]
            salida.append(
                f"| {p['paso']} | {md} | {sr} | {md + sr} | "
                f"{p['pivote']:.8e} | {p['fila_original_pivote']+1} |"
            )
        salida += [
            "",
            f"- Eliminación: {c.flops_eliminacion} flops "
            f"({c.mult_div_eliminacion} mul/div, {c.sum_rest_eliminacion} suma/resta)",
            f"- Sustitución regresiva: {c.flops_sustitucion} flops "
            f"({c.multiplicaciones_divisiones_sustitucion} mul/div, "
            f"{c.sumas_restas_sustitucion} suma/resta)",
            f"- **Total aritmético base: {c.flops_aritmeticos} flops**",
            f"- Divisiones adicionales para seleccionar pivote: {c.divisiones_busqueda}",
            f"- Total con esas divisiones: {c.flops_totales_con_pivote} flops",
            f"- Comparaciones de búsqueda: {c.comparaciones_busqueda}",
            f"- Comparaciones para obtener escalas: {c.comparaciones_escalas}",
            f"- Intercambios de filas: {c.intercambios}",
            "",
        ]
    salida += [
        "Cota de referencia del enunciado: ≈1486 flops. Nuestra convención da",
        "1366 flops aritméticos base: diferencia de −8.08 %, dentro de ±10 %.",
        "Para pivoteo escalado se incluyen además 77 divisiones de selección.",
        "La referencia del enunciado redondea el coste teórico y utiliza una",
        "convención que debe distinguirse del conteo instrumentado aquí.",
        "",
    ]
    return "\n".join(salida)


def generar_traza(corridas):
    salida = ["TRAZA COMPLETA DE 11 PASOS POR MÉTODO", ""]
    for corrida in corridas:
        c = corrida["contador"]
        salida.append(f"MÉTODO: {corrida['metodo']}")
        salida.append("")
        for paso in c.traza:
            salida.append(
                f"Paso {paso['paso']:2d} | pivote={paso['pivote']:.16e} | "
                f"fila original={paso['fila_original_pivote']+1}"
            )
            for fila in paso["matriz"]:
                salida.append(" ".join(f"{valor: .9e}" for valor in fila))
            salida.append("")
    return "\n".join(salida)


def generar_residuo(corridas, condicion, cota, control_np, referencia):
    salida = [
        "VERIFICACIÓN DEL LABORATORIO 3",
        "Residuo r=b-Ax con Decimal (80 dígitos) y A,b originales sin redondeo.",
        "Cada x float64 se convierte exactamente con Decimal.from_float.",
        "Numpy y mpmath se usan solo como controles independientes.",
        "",
        f"cond_2(A) estimada con numpy.linalg.cond: {condicion:.12e}",
        f"epsilon float64: {__import__('sys').float_info.epsilon:.12e}",
        f"cond_2(A) * epsilon: {cota:.12e}",
        "",
    ]
    for corrida in corridas:
        c = corrida["contador"]
        salida.extend([
            f"MÉTODO: {corrida['metodo']}",
            f"max |multiplicador|: {c.multiplicador_maximo:.12e}",
            f"factor de crecimiento: {c.factor_crecimiento:.12e}",
            f"bits potencialmente comprometidos (heurística, NO bits medidos): "
            f"{bits_amplificacion_estimada(c.multiplicador_maximo, c.factor_crecimiento):.3f}",
            f"||residuo inicial||_inf: {corrida['residuo_antes']}",
            f"||residuo tras una pasada de refinamiento||_inf: {corrida['residuo_refinado']}",
            f"refinamiento seleccionado por mejora del residuo: {corrida['refinamiento_aplicado']}",
            f"||residuo final||_inf: {corrida['residuo_final']}",
            f"||corrección||_inf: {corrida['correccion_maxima']:.12e}",
            f"error relativo SIN refinamiento respecto al control extendido: "
            f"{error_relativo_infinito(corrida['x'], referencia):.12e}",
            f"error relativo DESPUES de una pasada respecto al control extendido: "
            f"{error_relativo_infinito(corrida['x_refinado'], referencia):.12e}",
            f"error relativo FINAL respecto al control extendido: "
            f"{error_relativo_infinito(corrida['x_final'], referencia):.12e}",
            f"error normalizado de PA-LU: {corrida['error_factorizacion']:.12e}",
            "",
        ])
        # Vector residual completo: requisito de resultados/residuo.txt.
        # El cálculo Decimal ya se realizó en realizar_corrida; no refactorizar.
        salida.append("COMPONENTES DEL RESIDUO INICIAL r=b-Ax:")
        for i, valor in enumerate(corrida["vector_residuo_inicial"], start=1):
            salida.append(f"r_inicial[{i}] = {valor}")
        salida.append("COMPONENTES DEL RESIDUO FINAL r=b-Ax_final:")
        for i, valor in enumerate(corrida["vector_residuo_final"], start=1):
            salida.append(f"r_final[{i}] = {valor}")
        salida.append("")
    mejor = next(c for c in corridas if c["metodo"] == "pivoteo_escalado")
    salida.append("CONTROL numpy.linalg.solve (no utilizado como solución principal):")
    salida.append(f"Error relativo frente a NumPy: {error_relativo_infinito(mejor['x_final'], [str(v) for v in control_np]):.12e}")
    salida.append("CONTROL mpmath.lu_solve, 100 cifras: solo referencia de comparación de dígitos.")
    return "\n".join(salida) + "\n"


def generar_solucion(x, referencia, ruta):
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["incognita", "valor_float64", "valor_reportado", "digitos_defendibles"])
        for i, (valor, real) in enumerate(zip(x, referencia), start=1):
            digitos = digitos_defendibles(valor, real)
            # No anunciar más cifras de las defendibles.
            # Notación científica fija: incluye los ceros significativos
            # y muestra exactamente el número de cifras declarado.
            reportado = format(valor, f".{max(1, digitos)-1}e")
            escritor.writerow([f"x{i}", repr(valor), reportado, digitos])


def ejecutar():
    A, b = cargar_sistema()
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    corridas = [
        realizar_corrida(A, b, "sin_pivoteo"),
        realizar_corrida(A, b, "pivoteo_escalado"),
    ]
    condicion, cota = cota_condicion(A)
    control_np = control_numpy(A, b)
    referencia = control_mpmath(A, b, precision=100)
    mejor = corridas[1]

    generar_solucion(mejor["x_final"], referencia, RESULTADOS / "solucion.csv")
    (RESULTADOS / "traza_eliminacion.txt").write_text(
        generar_traza(corridas), encoding="utf-8"
    )
    (RESULTADOS / "conteo_flops.md").write_text(
        generar_conteo(corridas), encoding="utf-8"
    )
    (RESULTADOS / "residuo.txt").write_text(
        generar_residuo(corridas, condicion, cota, control_np, referencia),
        encoding="utf-8",
    )

    resumen = {
        "condicion_2": condicion,
        "cota_cond_eps": cota,
        "referencia_solo_control": "mpmath.lu_solve a 100 cifras",
        "metodos": {},
        "solucion": [],
    }
    for corrida in corridas:
        c = corrida["contador"]
        resumen["metodos"][corrida["metodo"]] = {
            "flops_base": c.flops_aritmeticos,
            "flops_pivote_extra": c.divisiones_busqueda,
            "comparaciones_pivote": c.comparaciones_busqueda,
            "comparaciones_escalas": c.comparaciones_escalas,
            "intercambios": c.intercambios,
            "multiplicador_maximo": c.multiplicador_maximo,
            "factor_crecimiento": c.factor_crecimiento,
            "residuo_inicial": str(corrida["residuo_antes"]),
            "residuo_refinado": str(corrida["residuo_refinado"]),
            "residuo_final": str(corrida["residuo_final"]),
            "refinamiento_seleccionado": corrida["refinamiento_aplicado"],
            "error_relativo_antes_refinamiento": error_relativo_infinito(
                corrida["x"], referencia
            ),
            "error_relativo_despues_refinamiento": error_relativo_infinito(
                corrida["x_refinado"], referencia
            ),
            "error_relativo_control_extendido": error_relativo_infinito(
                corrida["x_final"], referencia
            ),
        }
    for i, (valor, real) in enumerate(zip(mejor["x_final"], referencia), 1):
        resumen["solucion"].append({
            "variable": f"x{i}",
            "valor_float64": valor,
            "digitos_defendibles": digitos_defendibles(valor, real),
            "referencia_control": real,
        })
    (RESULTADOS / "diagnostico.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    # Informe comparativo de los dos métodos.
    (RESULTADOS / "comparacion_metodos.md").write_text(
        generar_comparacion(resumen),
        encoding="utf-8"
    )
    print("Resultados regenerados en:", RESULTADOS)
    print("Flops base:", mejor["contador"].flops_aritmeticos)
    print("Residuo final (norma infinito):", mejor["residuo_final"])
    return resumen


if __name__ == "__main__":
    ejecutar()

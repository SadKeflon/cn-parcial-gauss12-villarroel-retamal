
"""Comparación de los métodos de eliminación gaussiana."""

from decimal import Decimal


def cientifico(valor):
    """Convierte un valor a notación científica."""
    return f"{Decimal(str(valor)):.3E}"


def generar_comparacion(resumen):
    """Genera un informe Markdown con los resultados medidos."""

    metodos = resumen["metodos"]
    sin = metodos["sin_pivoteo"]
    con = metodos["pivoteo_escalado"]

    # Métricas que queremos comparar.
    filas = [
        ("Flops aritméticos base",
         sin["flops_base"], con["flops_base"], str),

        ("Divisiones adicionales de pivoteo",
         sin["flops_pivote_extra"],
         con["flops_pivote_extra"], str),

        ("Comparaciones de búsqueda",
         sin["comparaciones_pivote"],
         con["comparaciones_pivote"], str),

        ("Comparaciones para escalas",
         sin["comparaciones_escalas"],
         con["comparaciones_escalas"], str),

        ("Intercambios de filas",
         sin["intercambios"], con["intercambios"], str),

        ("Multiplicador máximo",
         sin["multiplicador_maximo"],
         con["multiplicador_maximo"], cientifico),

        ("Factor de crecimiento",
         sin["factor_crecimiento"],
         con["factor_crecimiento"], cientifico),

        ("Residuo inicial",
         sin["residuo_inicial"],
         con["residuo_inicial"], cientifico),

        ("Residuo final",
         sin["residuo_final"],
         con["residuo_final"], cientifico),

        ("Error relativo inicial",
         sin["error_relativo_antes_refinamiento"],
         con["error_relativo_antes_refinamiento"],
         cientifico),

        ("Error relativo final",
         sin["error_relativo_control_extendido"],
         con["error_relativo_control_extendido"],
         cientifico),
    ]

    lineas = [
        "# Comparación de los métodos de eliminación gaussiana",
        "",
        "Se utiliza el sistema original de 12 ecuaciones.",
        "",
        "| Indicador | Sin pivoteo | Pivoteo escalado |",
        "|---|---:|---:|",
    ]

    for nombre, valor_sin, valor_con, formato in filas:
        lineas.append(
            f"| {nombre} | {formato(valor_sin)} | "
            f"{formato(valor_con)} |"
        )

    residuo_sin = Decimal(str(sin["residuo_inicial"]))
    residuo_con = Decimal(str(con["residuo_inicial"]))

    crecimiento_sin = Decimal(
        str(sin["factor_crecimiento"])
    )
    crecimiento_con = Decimal(
        str(con["factor_crecimiento"])
    )

    lineas.extend([
        "",
        "## Interpretación de los resultados",
        "",
        f"- Sin pivoteo se realizaron {sin['flops_base']} "
        "flops aritméticos base.",

        f"- Con pivoteo escalado se realizaron "
        f"{con['flops_base']} flops base y "
        f"{con['flops_pivote_extra']} divisiones "
        "adicionales para seleccionar pivotes.",

        f"- El método escalado realizó "
        f"{con['intercambios']} intercambios de filas.",

        f"- La estimación de condición es "
        f"{cientifico(resumen['condicion_2'])}.",
    ])

    if crecimiento_con < crecimiento_sin and crecimiento_con != 0:
        factor = crecimiento_sin / crecimiento_con

        lineas.append(
            "- El factor de crecimiento sin pivoteo fue "
            f"{cientifico(factor)} veces el del "
            "pivoteo escalado."
        )
    else:
        lineas.append(
            "- El pivoteo no redujo el factor de crecimiento "
            "en esta ejecución."
        )

    if residuo_con < residuo_sin and residuo_con != 0:
        factor = residuo_sin / residuo_con

        lineas.append(
            "- Antes del refinamiento, el residuo sin "
            f"pivoteo fue {cientifico(factor)} veces "
            "mayor que el residuo con pivoteo escalado."
        )
    else:
        lineas.append(
            "- El residuo inicial con pivoteo no fue "
            "menor que el obtenido sin pivoteo."
        )

    lineas.extend([
        "",
        "## Consideraciones",
        "",
        "- Las comparaciones y los intercambios se "
        "informan por separado de las flops.",
        "- Los residuos finales corresponden a las "
        "soluciones seleccionadas después del refinamiento.",
        "- Un residuo pequeño no garantiza por sí solo "
        "una solución precisa cuando la matriz está "
        "mal condicionada.",
        "- NumPy y mpmath se usan solamente como "
        "controles independientes.",
        "",
        "Informe generado automáticamente con "
        "`python src/main.py`.",
        "",
    ])

    return "\n".join(lineas)

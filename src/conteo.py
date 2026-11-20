"""Contadores de operaciones instrumentados durante la ejecución real."""

from dataclasses import dataclass, field
from math import isfinite


@dataclass
class ContadorOperaciones:
    """Cuenta una flop por suma, resta, multiplicación o división.

    Comparaciones e intercambios se reportan aparte. La norma de crecimiento
    observa las matrices intermedias, no solamente la U final.
    """

    nombre: str
    pasos: list = field(default_factory=list)
    multiplicaciones_divisiones_sustitucion: int = 0
    sumas_restas_sustitucion: int = 0
    divisiones_busqueda: int = 0
    comparaciones_busqueda: int = 0
    comparaciones_escalas: int = 0
    intercambios: int = 0
    multiplicador_maximo: float = 0.0
    maximo_inicial: float = 0.0
    maximo_durante: float = 0.0
    traza: list = field(default_factory=list)

    def iniciar(self, matriz):
        self.maximo_inicial = max(abs(valor) for fila in matriz for valor in fila)
        self.maximo_durante = self.maximo_inicial

    def abrir_paso(self, k):
        self.pasos.append({
            "paso": k + 1,
            "multiplicaciones_divisiones": 0,
            "sumas_restas": 0,
            "pivote": None,
            "fila_original_pivote": None,
            "maximo_matriz": None,
        })

    def multiplicacion_division(self, k):
        self.pasos[k]["multiplicaciones_divisiones"] += 1

    def suma_resta(self, k):
        self.pasos[k]["sumas_restas"] += 1

    def multiplicador(self, valor):
        self.multiplicador_maximo = max(self.multiplicador_maximo, abs(valor))

    def costo_escalas(self, n):
        # n-1 comparaciones para cada una de las n escalas.
        self.comparaciones_escalas += n * (n - 1)

    def costo_busqueda(self, k, candidatos):
        # Cada candidato evalúa abs(U[i][k]) / escala[i].
        self.divisiones_busqueda += candidatos
        self.comparaciones_busqueda += candidatos - 1

    def intercambio(self):
        self.intercambios += 1

    def cerrar_paso(self, k, U, pivote, fila_original_pivote):
        maximo = max(abs(valor) for fila in U for valor in fila)
        if not isfinite(maximo):
            raise ArithmeticError("Apareció un valor no finito durante eliminación")
        self.maximo_durante = max(self.maximo_durante, maximo)
        self.pasos[k]["pivote"] = pivote
        self.pasos[k]["fila_original_pivote"] = fila_original_pivote
        self.pasos[k]["maximo_matriz"] = maximo
        self.traza.append({
            "paso": k + 1,
            "pivote": pivote,
            "fila_original_pivote": fila_original_pivote,
            "matriz": [fila.copy() for fila in U],
        })

    def producto_sustitucion(self):
        self.multiplicaciones_divisiones_sustitucion += 1

    def suma_sustitucion(self):
        self.sumas_restas_sustitucion += 1

    @property
    def mult_div_eliminacion(self):
        return sum(p["multiplicaciones_divisiones"] for p in self.pasos)

    @property
    def sum_rest_eliminacion(self):
        return sum(p["sumas_restas"] for p in self.pasos)

    @property
    def flops_eliminacion(self):
        return self.mult_div_eliminacion + self.sum_rest_eliminacion

    @property
    def flops_sustitucion(self):
        return self.multiplicaciones_divisiones_sustitucion + self.sumas_restas_sustitucion

    @property
    def flops_aritmeticos(self):
        # El cociente de búsqueda escalada se informa como sobrecosto separado.
        return self.flops_eliminacion + self.flops_sustitucion

    @property
    def flops_totales_con_pivote(self):
        return self.flops_aritmeticos + self.divisiones_busqueda

    @property
    def factor_crecimiento(self):
        return self.maximo_durante / self.maximo_inicial if self.maximo_inicial else 0.0

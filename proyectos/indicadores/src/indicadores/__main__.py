"""CLI mínima: python -m indicadores <indicador> ...

Ejemplos:
    python -m indicadores aprobacion "Cálculo I" 2026-1
    python -m indicadores desercion "Ingeniería de Sistemas" 2021-1 2026-1
    python -m indicadores promedio E10001
"""
from __future__ import annotations

import sys

from .calculos import promedio_ponderado, tasa_aprobacion, tasa_desercion
from .datos import cargar_calificaciones, cargar_matriculas


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    indicador, *args = argv
    if indicador == "aprobacion" and len(args) in (2, 3):
        print(f"{tasa_aprobacion(cargar_calificaciones(), *args):.2%}")
    elif indicador == "desercion" and len(args) == 3:
        print(f"{tasa_desercion(cargar_matriculas(), *args):.2%}")
    elif indicador == "promedio" and len(args) in (1, 2):
        print(promedio_ponderado(cargar_calificaciones(), *args))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

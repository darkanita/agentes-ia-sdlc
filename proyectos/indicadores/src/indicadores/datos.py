"""Carga de los datos sintéticos de calificaciones y matrículas."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

CARPETA_DATOS = Path(__file__).resolve().parents[2] / "datos"


@dataclass(frozen=True)
class Calificacion:
    periodo: str
    programa: str
    asignatura: str
    codigo_estudiante: str
    creditos: int
    nota_final: float


@dataclass(frozen=True)
class Matricula:
    codigo_estudiante: str
    programa: str
    cohorte: str
    periodo: str
    estado: str  # matriculado | retirado | graduado


def cargar_calificaciones(ruta: Path | None = None) -> list[Calificacion]:
    ruta = ruta or CARPETA_DATOS / "calificaciones.csv"
    with open(ruta, encoding="utf-8") as f:
        return [Calificacion(periodo=r["periodo"], programa=r["programa"], asignatura=r["asignatura"],
                             codigo_estudiante=r["codigo_estudiante"], creditos=int(r["creditos"]),
                             nota_final=float(r["nota_final"]))
                for r in csv.DictReader(f)]


def cargar_matriculas(ruta: Path | None = None) -> list[Matricula]:
    ruta = ruta or CARPETA_DATOS / "matriculas.csv"
    with open(ruta, encoding="utf-8") as f:
        return [Matricula(**r) for r in csv.DictReader(f)]

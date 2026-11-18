"""Indicadores académicos de la plataforma de inteligencia institucional.

Escala de notas de 0.0 a 5.0. Una asignatura se aprueba con nota final de 3.0 o más.
"""
from __future__ import annotations

from .datos import Calificacion, Matricula

NOTA_APROBATORIA = 3.0


def aprobo(nota_final: float) -> bool:
    """True si la nota final aprueba la asignatura."""
    return nota_final > NOTA_APROBATORIA


def tasa_aprobacion(calificaciones: list[Calificacion], asignatura: str, periodo: str,
                    programa: str | None = None) -> float:
    """Proporción de estudiantes que aprobaron la asignatura en el periodo (0 a 1, 4 decimales).

    Si se indica programa, solo cuenta a los estudiantes de ese programa.
    Lanza ValueError si no hay calificaciones para esa combinación.
    """
    notas = [c.nota_final for c in calificaciones
             if c.asignatura == asignatura and c.periodo == periodo
             and (programa is None or c.programa == programa)]
    if not notas:
        raise ValueError(f"No hay calificaciones de {asignatura} en {periodo}")
    return round(sum(aprobo(n) for n in notas) / len(notas), 4)


def promedio_ponderado(calificaciones: list[Calificacion], codigo_estudiante: str,
                       periodo: str | None = None) -> float:
    """Promedio de notas ponderado por créditos (2 decimales). Si no se indica periodo, es el acumulado."""
    propias = [c for c in calificaciones if c.codigo_estudiante == codigo_estudiante
               and (periodo is None or c.periodo == periodo)]
    if not propias:
        raise ValueError(f"No hay calificaciones del estudiante {codigo_estudiante}")
    creditos = sum(c.creditos for c in propias)
    return round(sum(c.nota_final * c.creditos for c in propias) / creditos, 2)


def tasa_desercion(matriculas: list[Matricula], programa: str, cohorte: str, periodo: str) -> float:
    """Proporción de la cohorte que desertó: no está matriculada en el periodo y no se graduó.

    Los graduados no son desertores. Resultado de 0 a 1 con 4 decimales.
    """
    cohorte_programa = {m.codigo_estudiante for m in matriculas
                        if m.programa == programa and m.cohorte == cohorte}
    if not cohorte_programa:
        raise ValueError(f"No hay estudiantes de la cohorte {cohorte} en {programa}")
    matriculados = {m.codigo_estudiante for m in matriculas
                    if m.periodo == periodo and m.estado == "matriculado"}
    desertores = cohorte_programa - matriculados
    return round(len(desertores) / len(cohorte_programa), 4)


def programas(calificaciones: list[Calificacion]) -> list[str]:
    return sorted({c.programa for c in calificaciones})


def asignaturas(calificaciones: list[Calificacion], programa: str | None = None) -> list[str]:
    return sorted({c.asignatura for c in calificaciones if programa is None or c.programa == programa})


def periodos(calificaciones: list[Calificacion]) -> list[str]:
    return sorted({c.periodo for c in calificaciones})

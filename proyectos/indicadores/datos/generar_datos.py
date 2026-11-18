"""Genera los datos sintéticos del proyecto (siempre los mismos: semilla fija).

Uso:
    python datos/generar_datos.py

Escribe calificaciones.csv y matriculas.csv en esta carpeta. No hay personas reales:
los códigos de estudiante son inventados y no hay nombres ni documentos.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SEMILLA = 2026

PROGRAMAS = {
    "Ingeniería de Sistemas": ["Cálculo I", "Programación I", "Álgebra Lineal", "Física I"],
    "Ingeniería Industrial": ["Cálculo I", "Estadística I", "Física I", "Dibujo Técnico"],
    "Administración Ambiental": ["Cálculo I", "Química General", "Estadística I", "Ecología"],
}
CREDITOS = {"Cálculo I": 4, "Programación I": 3, "Álgebra Lineal": 3, "Física I": 4,
            "Estadística I": 3, "Dibujo Técnico": 2, "Química General": 3, "Ecología": 2}
PERIODOS = ["2025-2", "2026-1"]


def nota(rng: random.Random) -> float:
    return round(min(5.0, max(0.0, rng.gauss(3.4, 0.8))), 1)


def generar() -> tuple[list[dict], list[dict]]:
    rng = random.Random(SEMILLA)
    calificaciones: list[dict] = []
    matriculas: list[dict] = []
    consecutivo = 10000

    for i, (programa, asignaturas) in enumerate(PROGRAMAS.items()):
        # Cohorte nueva (2025-2): cursa primer semestre y la mayoría sigue en 2026-1.
        for _ in range(40):
            consecutivo += 1
            codigo = f"E{consecutivo}"
            matriculas.append({"codigo_estudiante": codigo, "programa": programa, "cohorte": "2025-2",
                               "periodo": "2025-2", "estado": "matriculado"})
            sigue = rng.random() < 0.85
            matriculas.append({"codigo_estudiante": codigo, "programa": programa, "cohorte": "2025-2",
                               "periodo": "2026-1", "estado": "matriculado" if sigue else "retirado"})
            for periodo in PERIODOS if sigue else PERIODOS[:1]:
                for asignatura in asignaturas:
                    calificaciones.append({"periodo": periodo, "programa": programa, "asignatura": asignatura,
                                           "codigo_estudiante": codigo, "creditos": CREDITOS[asignatura],
                                           "nota_final": nota(rng)})

        # Cohorte antigua (2021-1): en 2025-2 unos se gradúan, otros siguen y otros se retiran.
        for j in range(30):
            consecutivo += 1
            codigo = f"E{consecutivo}"
            r = rng.random()
            estado_2025 = "graduado" if r < 0.40 else ("retirado" if r < 0.55 else "matriculado")
            matriculas.append({"codigo_estudiante": codigo, "programa": programa, "cohorte": "2021-1",
                               "periodo": "2025-2", "estado": estado_2025})
            if estado_2025 == "matriculado":
                continua = rng.random() < 0.8
                matriculas.append({"codigo_estudiante": codigo, "programa": programa, "cohorte": "2021-1",
                                   "periodo": "2026-1", "estado": "matriculado" if continua else "retirado"})

    # Cálculo I en 2026-1: varias notas quedan justo en el borde (3.0).
    borde = [c for c in calificaciones if c["asignatura"] == "Cálculo I" and c["periodo"] == "2026-1"]
    for c in rng.sample(borde, 9):
        c["nota_final"] = 3.0
    return calificaciones, matriculas


def escribir(filas: list[dict], nombre: str) -> None:
    with open(AQUI / nombre, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    cal, mat = generar()
    escribir(cal, "calificaciones.csv")
    escribir(mat, "matriculas.csv")
    print(f"calificaciones.csv: {len(cal)} filas · matriculas.csv: {len(mat)} filas")

"""Crea un repositorio git de práctica a partir de un proyecto de esta carpeta.

Uso:
    python proyectos/crear_repositorio.py DESTINO [--proyecto indicadores]

Copia el proyecto en DESTINO (que no debe existir), hace `git init` y arma un
historial corto de commits, como si el equipo lo hubiera construido por partes.
Así el agente de código puede leer también el historial (`git log`, `git blame`).
Solo usa la librería estándar y git.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
AUTOR = {"GIT_AUTHOR_NAME": "Equipo Analítica", "GIT_AUTHOR_EMAIL": "analitica@ejemplo.edu.co",
         "GIT_COMMITTER_NAME": "Equipo Analítica", "GIT_COMMITTER_EMAIL": "analitica@ejemplo.edu.co"}

# (fecha, mensaje, rutas que entran en ese commit)
HISTORIAL = {
    "indicadores": [
        ("2026-09-01T09:00:00", "Estructura inicial y carga de datos sintéticos",
         ["pyproject.toml", ".gitignore", "README.md", "datos", "src/indicadores/__init__.py",
          "src/indicadores/datos.py", "tests/test_datos.py"]),
        ("2026-09-10T15:30:00", "Indicadores: aprobación, promedio ponderado y deserción por cohorte",
         ["src/indicadores/calculos.py", "tests/test_calculos.py"]),
        ("2026-09-24T11:10:00", "CLI para consultar indicadores desde la terminal", ["."]),
    ],
}


def git(destino: Path, *args: str, fecha: str | None = None) -> None:
    env = {**os.environ, **AUTOR}
    if fecha:
        env |= {"GIT_AUTHOR_DATE": fecha, "GIT_COMMITTER_DATE": fecha}
    subprocess.run(["git", *args], cwd=destino, env=env, check=True, stdout=subprocess.DEVNULL)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("destino", type=Path)
    p.add_argument("--proyecto", default="indicadores", choices=sorted(HISTORIAL))
    a = p.parse_args()
    destino = a.destino.expanduser().resolve()
    if destino.exists():
        print(f"{destino} ya existe: bórrelo o elija otra carpeta.", file=sys.stderr)
        return 1
    origen = AQUI / a.proyecto
    shutil.copytree(origen, destino, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))
    git(destino, "init", "-q", "-b", "main")
    for fecha, mensaje, rutas in HISTORIAL[a.proyecto]:
        git(destino, "add", "--", *rutas)
        git(destino, "commit", "-q", "-m", mensaje, fecha=fecha)
    print(f"Repositorio listo en {destino} ({len(HISTORIAL[a.proyecto])} commits).")
    print(f"Siguiente paso: cd \"{destino}\" y luego opencode")
    return 0


if __name__ == "__main__":
    sys.exit(main())

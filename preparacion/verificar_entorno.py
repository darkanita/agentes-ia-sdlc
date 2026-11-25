"""Verifica que la máquina está lista para el curso. No cambia nada.

Uso:
    python preparacion/verificar_entorno.py                  # versiones, paquetes, llaves y red
    python preparacion/verificar_entorno.py --probar-modelo  # además, una pregunta corta al modelo
"""
from __future__ import annotations

import argparse
import importlib
import os
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
VERDE, ROJO, AMARILLO, FIN = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
if os.name == "nt":
    os.system("")  # activa los colores ANSI en la consola de Windows

faltas = 0


def informe(estado: str, que: str, detalle: str = "") -> None:
    global faltas
    color = {"OK": VERDE, "FALTA": ROJO, "AVISO": AMARILLO}[estado]
    faltas += estado == "FALTA"
    print(f"  {color}{estado:<5}{FIN} {que}" + (f" — {detalle}" if detalle else ""))


def version(comando: list[str]) -> str | None:
    if not shutil.which(comando[0]):
        return None
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=20, shell=os.name == "nt")
        return (r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr) else ""
    except Exception:
        return None


def numero(texto: str | None) -> tuple[int, ...]:
    m = re.search(r"(\d+)\.(\d+)", texto or "")
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def herramientas() -> None:
    print("\nHerramientas")
    v = sys.version_info
    informe("OK" if v >= (3, 10) else "FALTA", f"Python {v.major}.{v.minor}", "" if v >= (3, 10) else "instale 3.10 o superior")
    g = version(["git", "--version"])
    informe("OK" if g else "FALTA", f"Git {g or ''}".strip(), "" if g else "instale Git")
    n = version(["node", "--version"])
    informe("OK" if n and numero(n) >= (20, 0) else "AVISO", f"Node.js {n or 'no encontrado'}",
            "" if n else "solo hace falta para instalar OpenCode con npm")
    o = version(["opencode", "--version"])
    if not o:
        informe("FALTA", "OpenCode", "npm install -g @opencode/cli (vea preparacion/README.md)")
    elif numero(o)[0] < 2:
        informe("AVISO", f"OpenCode {o}", "es la versión 1: el curso usa la 2 (npm install -g @opencode/cli)")
    else:
        informe("OK", f"OpenCode {o}")
    c = version(["code", "--version"])
    informe("OK" if c else "AVISO", f"VS Code {c or 'no encontrado'}", "" if c else "recomendado, no obligatorio")


def paquetes() -> None:
    print("\nPaquetes de Python")
    for nombre, modulo in [("openai", "openai"), ("python-dotenv", "dotenv"), ("pytest", "pytest")]:
        try:
            importlib.import_module(modulo)
            informe("OK", nombre)
        except ImportError:
            informe("FALTA", nombre, "python -m pip install -r requirements.txt")
    if not os.getenv("VIRTUAL_ENV"):
        informe("AVISO", "Entorno virtual", "no está activo (.venv); funciona, pero es mejor activarlo")


def llaves() -> dict[str, str]:
    print("\nLlaves (.env)")
    archivo = RAIZ / ".env"
    if not archivo.exists():
        informe("FALTA", ".env", "copie .env.ejemplo como .env y ponga sus llaves")
        return {}
    try:
        from dotenv import dotenv_values
        valores = {k: v for k, v in dotenv_values(archivo).items() if v}
    except ImportError:
        valores = {}
    tiene = [k for k in ("GROQ_API_KEY", "OPENROUTER_API_KEY") if valores.get(k)]
    for k in ("GROQ_API_KEY", "OPENROUTER_API_KEY"):
        informe("OK" if k in tiene else ("AVISO" if tiene else "FALTA"), k,
                "" if k in tiene else "créela en la consola del proveedor (preparacion/README.md, sección 3)")
    proveedor = valores.get("PROVEEDOR") or "groq"
    clave = {"groq": "GROQ_API_KEY", "openrouter": "OPENROUTER_API_KEY"}.get(proveedor)
    if clave and clave not in tiene and tiene:
        informe("AVISO", f"PROVEEDOR={proveedor}", f"pero no hay {clave}: cambie PROVEEDOR en .env")
    return valores


def red() -> None:
    print("\nConexión")
    for host in ["opencode.ai", "api.groq.com", "openrouter.ai", "pypi.org", "github.com"]:
        try:
            socket.create_connection((host, 443), timeout=5).close()
            informe("OK", host)
        except OSError:
            informe("FALTA", host, "sin conexión: revise la red o el proxy")


def probar_modelo(valores: dict[str, str]) -> None:
    print("\nModelo")
    proveedores = {"groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
                   "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "openrouter/free")}
    try:
        proveedor = valores.get("PROVEEDOR") or "groq"
        url, var, modelo = proveedores.get(proveedor, proveedores["groq"])
        if not valores.get(var):
            informe("FALTA", f"{proveedor}", f"falta {var} en .env")
            return
        from openai import OpenAI
        modelo = valores.get("MODELO") or modelo
        r = OpenAI(base_url=url, api_key=valores[var], timeout=40).chat.completions.create(
            model=modelo, messages=[{"role": "user", "content": "Responde solo: listo"}], max_tokens=200)
        informe("OK", f"{proveedor} · {modelo}", (r.choices[0].message.content or "").strip()[:40])
    except Exception as e:
        informe("FALTA", "Llamada al modelo", f"{type(e).__name__}: {str(e)[:160]}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--probar-modelo", action="store_true")
    a = p.parse_args()
    print("Verificación del entorno del curso")
    herramientas()
    paquetes()
    valores = llaves()
    red()
    if a.probar_modelo:
        probar_modelo(valores)
    print()
    if faltas:
        print(f"{ROJO}Faltan {faltas} punto(s).{FIN} Envíe esta captura por el canal del curso para resolverlo.")
        return 1
    print(f"{VERDE}Listo para el curso.{FIN} Envíe esta captura por el canal del curso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

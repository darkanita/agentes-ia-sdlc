"""Carga laboratorio/agente.py, o la solución de la docente si AGENTE_SOLUCION=1 (solo en su repositorio)."""
import importlib.util
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

SESION = Path(__file__).resolve().parents[2]
ARCHIVO = SESION / ("solucion" if os.getenv("AGENTE_SOLUCION") == "1" else "laboratorio") / "agente.py"
spec = importlib.util.spec_from_file_location("agente_lab", ARCHIVO)
agente = importlib.util.module_from_spec(spec)
sys.modules["agente_lab"] = agente
spec.loader.exec_module(agente)


def llamada(nombre, argumentos, id_="c1"):
    texto = argumentos if isinstance(argumentos, str) else json.dumps(argumentos)
    return NS(id=id_, type="function", function=NS(name=nombre, arguments=texto))


def respuesta(contenido=None, llamadas=None):
    return NS(choices=[NS(message=NS(content=contenido, tool_calls=llamadas))])


class LLMFalso:
    """Devuelve, en orden, las respuestas guionadas y guarda los mensajes que recibió en cada llamada."""
    def __init__(self, guion):
        self.guion = list(guion)
        self.recibido = []
        self.chat = NS(completions=self)

    def create(self, model, messages, tools=None, **_):
        self.recibido.append({"messages": [dict(m) for m in messages], "tools": tools})
        return self.guion.pop(0) if self.guion else respuesta("fin del guion")


@pytest.fixture
def mod():
    return agente

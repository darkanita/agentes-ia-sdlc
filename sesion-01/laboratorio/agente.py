"""Laboratorio 1 · Su primer harness: el ciclo del agente con controles.

Complete los TODO. Las pruebas usan un LLM falso, así que no necesita red ni llave:
    python -m pytest sesion-01/laboratorio/tests -q
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Herramienta:
    nombre: str
    descripcion: str
    funcion: Callable[..., Any]
    parametros: dict = field(default_factory=dict)   # nombre -> descripción
    requeridos: list[str] = field(default_factory=list)
    requiere_aprobacion: bool = False                # True: una persona debe aprobar cada uso

    def esquema(self) -> dict:
        """Descripción de la herramienta en el formato que entiende la API (tools de OpenAI)."""
        return {"type": "function", "function": {
            "name": self.nombre, "description": self.descripcion,
            "parameters": {"type": "object",
                           "properties": {p: {"type": "string", "description": d} for p, d in self.parametros.items()},
                           "required": self.requeridos}}}


@dataclass
class Resultado:
    respuesta: str
    pasos: int
    traza: list[dict]          # una entrada por cada herramienta usada: {"herramienta", "argumentos", "observacion"}
    terminado: bool            # False si se agotó max_pasos


def nunca_aprobar(nombre: str, argumentos: dict) -> bool:
    return False


class Agente:
    def __init__(self, cliente, modelo: str, herramientas: list[Herramienta], sistema: str = "",
                 max_pasos: int = 5, aprobador: Callable[[str, dict], bool] = nunca_aprobar):
        self.cliente = cliente
        self.modelo = modelo
        self.herramientas = {h.nombre: h for h in herramientas}
        self.sistema = sistema
        self.max_pasos = max_pasos
        self.aprobador = aprobador

    def ejecutar_herramienta(self, nombre: str, argumentos_json: str) -> str:
        """Ejecuta una herramienta y devuelve la observación como texto. Nunca lanza excepciones.

        - Herramienta que no existe        -> "ERROR: herramienta desconocida: <nombre>"
        - Argumentos que no son JSON válido -> "ERROR: argumentos inválidos"
        - Requiere aprobación y el aprobador dice que no -> "DENEGADO: la persona no aprobó <nombre>"
        - La función lanza una excepción    -> "ERROR: <TipoDeExcepcion>: <mensaje>"
        - Si todo sale bien                 -> json.dumps(resultado, ensure_ascii=False)
        """
        # TODO 1: implemente las cinco reglas del docstring.
        raise NotImplementedError("TODO 1")

    def ejecutar(self, pregunta: str) -> Resultado:
        """El ciclo razonar → actuar → observar.

        En cada paso: llama al modelo con los mensajes y los esquemas de las herramientas.
        - Si el mensaje no trae tool_calls, es la respuesta final: termina.
        - Si trae tool_calls: agrega el mensaje del asistente, ejecuta cada herramienta,
          agrega cada observación como mensaje role="tool" con su tool_call_id y la anota en la traza.
        Si se agotan max_pasos sin respuesta final, devuelve terminado=False y una respuesta que lo diga.
        """
        mensajes: list[dict] = []
        if self.sistema:
            mensajes.append({"role": "system", "content": self.sistema})
        mensajes.append({"role": "user", "content": pregunta})
        esquemas = [h.esquema() for h in self.herramientas.values()]
        traza: list[dict] = []

        # TODO 2: el ciclo. Pista: así se llama al modelo y se lee su mensaje:
        #   respuesta = self.cliente.chat.completions.create(model=self.modelo, messages=mensajes, tools=esquemas)
        #   mensaje = respuesta.choices[0].message      # mensaje.content, mensaje.tool_calls
        #   cada t en mensaje.tool_calls tiene t.id, t.function.name y t.function.arguments (texto JSON)
        # TODO 3: si se agotan los pasos, no siga: devuelva terminado=False.
        raise NotImplementedError("TODOs 2 y 3")

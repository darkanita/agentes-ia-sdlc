"""Un agente en ~100 líneas: un LLM, unas herramientas y el ciclo razonar → actuar → observar.

Responde preguntas sobre indicadores académicos usando las funciones del proyecto
proyectos/indicadores como herramientas. Imprime cada vuelta del ciclo.

Uso:
    python sesion-02/demo/agente_minimo.py "¿Cuál fue la tasa de aprobación de Cálculo I en 2026-1?"
    python sesion-02/demo/agente_minimo.py --simulado          # sin red ni llave: un "LLM" guionado
    python sesion-02/demo/agente_minimo.py --proyecto ../practica-indicadores "..."   # usa otro código

Proveedor y modelo se leen de .env (vea .env.ejemplo): PROVEEDOR=groq|openrouter, MODELO=...
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace as NS

RAIZ = Path(__file__).resolve().parents[2]
PROVEEDORES = {  # los dos exponen una API compatible con la de OpenAI
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "openrouter/free"),
}
SISTEMA = ("Eres un analista de la oficina de planeación de una universidad. Responde en español y en pocas "
           "líneas. Usa SIEMPRE las herramientas para obtener cifras; nunca inventes un número. "
           "Si una herramienta devuelve un error, explícalo.")
MAX_PASOS = 6


def herramientas(proyecto: Path):
    """Las funciones que el agente puede usar y su descripción para el modelo."""
    sys.path.insert(0, str(proyecto / "src"))
    from indicadores import calculos as k
    from indicadores.datos import cargar_calificaciones, cargar_matriculas
    cal = cargar_calificaciones(proyecto / "datos" / "calificaciones.csv")
    mat = cargar_matriculas(proyecto / "datos" / "matriculas.csv")
    funciones = {
        "listar_opciones": lambda: {"programas": k.programas(cal), "asignaturas": k.asignaturas(cal),
                                    "periodos": k.periodos(cal), "cohortes": sorted({m.cohorte for m in mat})},
        "tasa_aprobacion": lambda asignatura, periodo, programa=None: k.tasa_aprobacion(cal, asignatura, periodo, programa),
        "tasa_desercion": lambda programa, cohorte, periodo: k.tasa_desercion(mat, programa, cohorte, periodo),
    }
    def f(nombre, desc, props, req):
        return {"type": "function", "function": {"name": nombre, "description": desc,
                "parameters": {"type": "object", "properties": {p: {"type": "string"} for p in props}, "required": req}}}
    esquemas = [
        f("listar_opciones", "Programas, asignaturas, periodos y cohortes disponibles.", [], []),
        f("tasa_aprobacion", "Proporción (0 a 1) de aprobados de una asignatura en un periodo, opcionalmente por programa.",
          ["asignatura", "periodo", "programa"], ["asignatura", "periodo"]),
        f("tasa_desercion", "Proporción (0 a 1) de una cohorte de un programa que desertó en un periodo.",
          ["programa", "cohorte", "periodo"], ["programa", "cohorte", "periodo"]),
    ]
    return funciones, esquemas


def cliente_real():
    from dotenv import load_dotenv
    from openai import OpenAI
    load_dotenv(RAIZ / ".env")
    proveedor = os.getenv("PROVEEDOR", "groq")
    url, var_llave, modelo = PROVEEDORES[proveedor]
    if not os.getenv(var_llave):
        sys.exit(f"Falta {var_llave} en .env. Use --simulado o vea preparacion/README.md.")
    return OpenAI(base_url=url, api_key=os.environ[var_llave]), os.getenv("MODELO", modelo), proveedor


class ClienteSimulado:
    """Un 'LLM' guionado: primero pide la herramienta y luego redacta con lo que observó."""
    def __init__(self):
        self.chat = NS(completions=self)

    def create(self, messages, **_):
        ultimo = messages[-1]
        if ultimo["role"] == "user":
            llamada = NS(id="sim-1", type="function", function=NS(name="tasa_aprobacion",
                         arguments=json.dumps({"asignatura": "Cálculo I", "periodo": "2026-1"}, ensure_ascii=False)))
            msg = NS(content="Necesito la tasa de aprobación: llamo a la herramienta.", tool_calls=[llamada])
        else:
            msg = NS(content=f"La tasa de aprobación de Cálculo I en 2026-1 fue {float(ultimo['content']):.1%}.",
                     tool_calls=None)
        return NS(choices=[NS(message=msg)], usage=NS(prompt_tokens=0, completion_tokens=0))


def ejecutar(pregunta: str, cliente, modelo: str, funciones, esquemas) -> str:
    mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pregunta}]
    for paso in range(1, MAX_PASOS + 1):
        r = cliente.chat.completions.create(model=modelo, messages=mensajes, tools=esquemas)
        msg, uso = r.choices[0].message, r.usage
        print(f"\n── Vuelta {paso} · tokens: {uso.prompt_tokens} entrada + {uso.completion_tokens} salida")
        if not msg.tool_calls:  # sin herramientas que llamar: es la respuesta final
            return msg.content
        razonamiento = msg.content or getattr(msg, "reasoning", None)  # algunos modelos lo envían aparte
        if razonamiento:
            print(f"   RAZONAR  {razonamiento.strip()[:300]}")
        mensajes.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
            {"id": t.id, "type": "function", "function": {"name": t.function.name, "arguments": t.function.arguments}}
            for t in msg.tool_calls]})
        for t in msg.tool_calls:
            print(f"   ACTUAR   {t.function.name}({t.function.arguments})")
            try:
                resultado = funciones[t.function.name](**json.loads(t.function.arguments or "{}"))
            except Exception as e:  # el error también es una observación: el modelo puede corregirse
                resultado = f"ERROR: {type(e).__name__}: {e}"
            print(f"   OBSERVAR {str(resultado)[:300]}")
            mensajes.append({"role": "tool", "tool_call_id": t.id, "content": json.dumps(resultado, ensure_ascii=False)})
    return f"No terminé en {MAX_PASOS} vueltas (el límite es un control del harness)."


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pregunta", nargs="?", default="¿Cuál fue la tasa de aprobación de Cálculo I en 2026-1?")
    p.add_argument("--simulado", action="store_true", help="sin red: un LLM guionado")
    p.add_argument("--proyecto", type=Path, default=RAIZ / "proyectos" / "indicadores")
    a = p.parse_args()
    funciones, esquemas = herramientas(a.proyecto.expanduser().resolve())
    if a.simulado:
        cliente, modelo, proveedor = ClienteSimulado(), "simulado", "simulado"
    else:
        cliente, modelo, proveedor = cliente_real()
    print(f"Pregunta: {a.pregunta}\nModelo: {proveedor} · {modelo}")
    print(f"\nRESPUESTA: {ejecutar(a.pregunta, cliente, modelo, funciones, esquemas)}")


if __name__ == "__main__":
    main()

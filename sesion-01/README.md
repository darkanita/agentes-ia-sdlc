# Sesión 1 — Agentes en el SDLC y SDLC de agentes: qué son, qué ganan y dónde fallan

**2 horas**

## Objetivo

Entender qué es un agente de IA (un modelo, unas herramientas y el ciclo razonar → actuar → observar), ver las dos direcciones del curso sobre un mismo caso y reconocer desde el primer día sus bondades, sus límites y sus riesgos.

| Dirección | Pregunta | Hoy lo vemos con |
|---|---|---|
| **1. Agentes en el SDLC** | ¿Cómo me ayuda un agente de código a entender, corregir y probar software? | OpenCode sobre el repositorio `indicadores` |
| **2. El SDLC de un agente** | ¿Cómo construyo, pruebo y opero un producto que *es* un agente? | `demo/agente_minimo.py`, un agente que responde preguntas sobre indicadores |

Las dos usan el mismo código: cuando el agente de código corrige un indicador, el agente producto empieza a responder bien.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:12 | Apertura: el curso, las dos direcciones, el proyecto por parejas y las reglas de datos | Presentación |
| 0:12 – 0:32 | Qué es un agente: modelo + herramientas + ciclo + harness | Presentación + `demo/agente_minimo.py` |
| 0:32 – 0:47 | OpenCode: qué es, modelos gratuitos, agentes Build y Plan, permisos y `AGENTS.md` | Presentación + OpenCode |
| 0:47 – 1:22 | En vivo: un reporte de error de punta a punta con un agente de código | `proyectos/indicadores` |
| 1:22 – 1:40 | Bondades y límites: alucinación, datos sensibles, capas gratuitas, cuándo no usar un agente | Presentación + OpenCode |
| 1:40 – 1:52 | Primer mapa de casos de uso por pareja | `autonomo/FICHA_CASO.md` |
| 1:52 – 2:00 | Cómo llegar listos a la sesión 2 | `preparacion/`, `autonomo/` |

## Archivos

```
sesion-01/
├── demo/
│   ├── agente_minimo.py       un agente de ~100 líneas: imprime cada vuelta del ciclo
│   ├── opencode.json          permisos que piden aprobación (OpenCode 2)
│   └── opencode-v1.json       lo mismo para OpenCode 1
├── laboratorio/               Laboratorio 1: su primer harness (con pruebas, sin red)
│   ├── ENUNCIADO.md
│   ├── agente.py              plantilla con TODOs
│   └── tests/                 15 pruebas con un LLM falso
└── autonomo/
    ├── INSTRUCCIONES.md       trabajo para antes de la sesión 2
    ├── BITACORA.md
    └── FICHA_CASO.md          candidato a caso de proyecto de la pareja
```

## Ejecutar

```bash
python sesion-01/demo/agente_minimo.py --simulado            # sin red ni llave
python sesion-01/demo/agente_minimo.py "¿Qué tasa de deserción tuvo la cohorte 2021-1 de Ingeniería de Sistemas en 2026-1?"
python proyectos/crear_repositorio.py ../practica-indicadores  # repositorio de práctica con historial
python -m pytest sesion-01/laboratorio/tests -q              # al inicio fallan las 15: es lo esperado
```

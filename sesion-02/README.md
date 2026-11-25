# Sesión 2 — Manos a la obra: el ciclo del agente y un agente de código en un repositorio real

**2 horas** · Requisito: tener la máquina lista ([`preparacion/README.md`](../preparacion/README.md)).

## Objetivo

Poner en práctica lo que vimos en la sesión 1: ver el ciclo razonar → actuar → observar en código, usar OpenCode para llevar un reporte de error de punta a punta con aprobación humana, y elegir el caso de proyecto de cada pareja.

| Dirección | Pregunta | Hoy lo hacemos con |
|---|---|---|
| **1. Agentes en el SDLC** | ¿Cómo me ayuda un agente de código a entender, corregir y probar software? | OpenCode sobre el repositorio `indicadores` |
| **2. El SDLC de un agente** | ¿Cómo construyo, pruebo y opero un producto que *es* un agente? | `demo/agente_minimo.py`, un agente que responde preguntas sobre indicadores |

Las dos usan el mismo código: cuando el agente de código corrige un indicador, el agente producto empieza a responder bien.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Entornos listos: verificador y primer `opencode` | `preparacion/verificar_entorno.py` |
| 0:10 – 0:25 | El ciclo en código: un agente en ~100 líneas | `demo/agente_minimo.py` |
| 0:25 – 0:40 | OpenCode en su repositorio: modelos, Build y Plan, permisos | `demo/opencode.json` |
| 0:40 – 1:15 | En vivo y en parejas: un reporte de error de punta a punta | `proyectos/indicadores` |
| 1:15 – 1:25 | Los límites, en vivo: alucinación y datos sensibles | OpenCode |
| 1:25 – 1:50 | **Hito 1:** el caso de cada pareja | `autonomo/` de la sesión 1 |
| 1:50 – 2:00 | Laboratorio 1 y trabajo autónomo | `laboratorio/`, `autonomo/` |

## Archivos

```
sesion-02/
├── demo/
│   ├── agente_minimo.py       un agente de ~100 líneas: imprime cada vuelta del ciclo
│   ├── opencode.json          permisos que piden aprobación (OpenCode 2)
│   └── opencode-v1.json       lo mismo para OpenCode 1
├── laboratorio/               Laboratorio 1: su primer harness (con pruebas, sin red)
│   ├── ENUNCIADO.md
│   ├── agente.py              plantilla con TODOs
│   └── tests/                 15 pruebas con un LLM falso
└── autonomo/
    ├── INSTRUCCIONES.md       trabajo para antes de la sesión 3
    └── BITACORA.md
```

## Ejecutar

```bash
python sesion-02/demo/agente_minimo.py --simulado            # sin red ni llave
python sesion-02/demo/agente_minimo.py "¿Qué tasa de deserción tuvo la cohorte 2021-1 de Ingeniería de Sistemas en 2026-1?"
python proyectos/crear_repositorio.py ../practica-indicadores  # repositorio de práctica con historial
python -m pytest sesion-02/laboratorio/tests -q              # al inicio fallan las 15: es lo esperado
```

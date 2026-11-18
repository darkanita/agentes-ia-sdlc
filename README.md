# Fundamentos de agentes de IA y sistemas multiagente — Laboratorios

Material práctico del curso: **20 horas, 10 sesiones de 2 horas**.

El curso trabaja en dos direcciones del ciclo de vida del software, sobre el mismo caso:

1. **Agentes en el SDLC:** usar agentes de código para requisitos, diseño, codificación, pruebas, revisión, despliegue y operación.
2. **El SDLC de un agente:** diseñar, construir, evaluar, desplegar y operar productos que son agentes o sistemas multiagente.

En las dos, el centro es el **harness** que controla al agente: contexto, herramientas, permisos y verificación, con supervisión humana.

**Todo con herramientas abiertas y capas gratuitas, sin licencias:** [OpenCode](https://opencode.ai) como agente de código, modelos gratuitos de OpenCode Zen, Groq y OpenRouter, Python, GitHub y GitHub Actions. **Solo datos de prueba:** ningún laboratorio usa información institucional.

## Cómo está organizada cada sesión

| Carpeta | Para qué |
|---|---|
| `demo/` | Lo que la docente muestra en vivo |
| `laboratorio/` | El ejercicio de la sesión, con pruebas automáticas |
| `autonomo/` | Trabajo para antes de la siguiente sesión |
| `proyectos/` | Proyectos de práctica con datos sintéticos que se reutilizan en varias sesiones |

Las presentaciones se publican en `slides/pdf/` después de cada sesión.

## Preparación del entorno (una sola vez)

Siga [`preparacion/README.md`](preparacion/README.md) y verifique su máquina:

```bash
python preparacion/verificar_entorno.py --probar-modelo
```

## Cronograma

Proyecto aplicado en **parejas mixtas** (una persona del proyecto y una de Sistemas): un producto agéntico pequeño, construido con ayuda de agentes de código.

| Sesión | Tema | Dirección | Hito de la pareja |
|---|---|---|---|
| 1 | Qué es un agente y el ciclo razonar–actuar–observar; OpenCode en un repositorio real; bondades y límites | Las dos | — |
| 2 | Valor, límites y riesgos con casos reales; mapa de casos de uso priorizados | Las dos | **Hito 1:** caso elegido |
| 3 | El harness I: instrucciones y contexto (`AGENTS.md`, reglas), modelos y costos | 1 | — |
| 4 | El harness II: herramientas y MCP, permisos y aprobación, sandbox y hooks; el harness del producto | 1 y 2 | **Hito 2:** harness diseñado |
| 5 | De la historia de usuario a la especificación y al plan con agentes de código; herramientas del agente producto | 1 y 2 | — |
| 6 | Flujo multiagente supervisado (planificador, ejecutor, revisor); pruebas generadas y revisión humana | 2 | **Hito 3:** producto funcionando |
| 7 | Harness de evaluación: casos, criterios de aceptación y métricas en GitHub Actions | 2 | — |
| 8 | Operar: observabilidad, trazabilidad, costos, seguridad (inyección de instrucciones, información sensible) y gobierno | 2 | **Hito 4:** evaluación en CI |
| 9 | Taller del proyecto aplicado y guía de adopción | Las dos | — |
| 10 | Presentación por parejas y hoja de ruta de adopción | Las dos | **Entrega final** |

Se recomienda conocimiento básico de Python y Git.

## Proyectos de práctica

[`proyectos/indicadores`](proyectos/indicadores) calcula indicadores académicos (aprobación, promedio ponderado, deserción) con datos sintéticos. Para practicar sobre un repositorio git con historial:

```bash
python proyectos/crear_repositorio.py ../practica-indicadores
```

## Material de referencia

Lecturas opcionales por sesión en [`REFERENCIAS.md`](REFERENCIAS.md).

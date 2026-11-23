# Sesión 1 — Agentes de IA: qué son, cómo cambian el SDLC y qué cambia cuando el producto es un agente

**2 horas · sesión conceptual.** La práctica empieza en la sesión 2: para entonces su máquina debe estar lista (vea el trabajo autónomo).

## Objetivo

Construir un vocabulario común para el resto del curso: qué es un agente y en qué se diferencia de un chat o de un flujo fijo; cómo participan los agentes en cada etapa del ciclo de vida del software; qué cambia cuando lo que construimos *es* un agente; sus bondades, límites y riesgos; y con qué herramientas vamos a trabajar.

## Las dos direcciones del curso

| Dirección | Pregunta |
|---|---|
| **1. Agentes en el SDLC** | ¿Cómo me ayuda un agente de código a especificar, construir, probar, revisar y operar software? |
| **2. El SDLC de un agente** | ¿Cómo diseño, construyo, evalúo, despliego y opero un producto que *es* un agente o un sistema multiagente? |

En las dos, el centro es el **harness**: el contexto, las herramientas, los permisos y la verificación que rodean al modelo, con una persona que aprueba.

## Agenda

| Tiempo | Bloque |
|---|---|
| 0:00 – 0:12 | El curso: las dos direcciones, cómo trabajamos y la regla de los datos |
| 0:12 – 0:47 | **Qué es un agente:** definición y de dónde viene; el modelo, las herramientas y el llamado a herramientas; el ciclo razonar → actuar → observar; cómo razona (ReAct, planificar y ejecutar); contexto y memoria; MCP y A2A; tipos de agentes |
| 0:47 – 1:05 | **Sistemas y arquitecturas multiagente:** flujos y agentes; por qué más de un agente; roles; arquitecturas secuencial, supervisor, jerárquica y en red; cómo se coordinan; dos ejemplos; lo que se complica; marcos |
| 1:05 – 1:17 | Agentes en el SDLC: qué hacen en cada etapa, niveles de autonomía y dónde aprueba una persona |
| 1:17 – 1:25 | El SDLC de un agente: qué cambia cuando el producto es un agente |
| 1:25 – 1:37 | Bondades, límites y riesgos; cuándo **no** usar un agente |
| 1:37 – 1:47 | Las herramientas del curso: OpenCode, modelos gratuitos, Python y GitHub |
| 1:47 – 1:55 | Primer mapa de casos de uso por pareja |
| 1:55 – 2:00 | Cómo llegar listos a la sesión 2 |

## Conceptos clave

| Término | En una línea |
|---|---|
| **Agente** | Un modelo de lenguaje que, en un ciclo, decide qué herramientas usar, observa los resultados y sigue hasta terminar una tarea. |
| **Herramienta** | Una función con nombre y descripción que el agente puede pedir: leer un archivo, ejecutar pruebas, consultar un dato. El modelo la pide; el código la ejecuta. |
| **Ciclo razonar → actuar → observar** | Cada vuelta: el modelo decide, pide una herramienta, recibe el resultado y vuelve a decidir. |
| **Flujo (workflow)** | Pasos fijos definidos por una persona, aunque alguno use un modelo. Más predecible y barato que un agente. |
| **Sistema multiagente** | Varios agentes con roles (planificador, ejecutor, revisor) que se pasan trabajo entre sí. |
| **Supervisor** | Arquitectura multiagente en la que un agente coordina y reparte el trabajo a agentes especialistas. |
| **Harness** | Todo lo que rodea al modelo: instrucciones, contexto, herramientas, permisos, límites, aprobación humana y verificación. |
| **Agente de código** | Un agente cuyas herramientas son las del desarrollo: leer, buscar, editar, ejecutar comandos. En el curso: OpenCode. |
| **Evaluación** | Medir con casos y criterios si un agente responde bien, de forma repetible. Es a un agente lo que las pruebas al código. |
| **ReAct** | Estrategia en la que el modelo intercala pensamiento, acción y observación en cada paso. |
| **Contexto** | Todo lo que el modelo recibe en una llamada: instrucciones, conversación, archivos y resultados de herramientas. |
| **MCP** | Model Context Protocol: estándar abierto para conectar un agente con herramientas y datos. |
| **A2A** | Agent2Agent: estándar abierto para que agentes de distintos proveedores se comuniquen y deleguen tareas. |

## Antes de la sesión 2

Vea [`autonomo/INSTRUCCIONES.md`](autonomo/INSTRUCCIONES.md): preparar la máquina, una lectura corta y dos ideas de caso por pareja.

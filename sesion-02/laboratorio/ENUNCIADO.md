# Laboratorio 1 · Su primer harness

En la demo vio un agente que funciona. Ahora usted escribe la parte que lo hace **confiable**: el código que rodea al modelo, decide qué herramientas puede usar, qué pasa cuando algo falla y cuándo detenerse. Eso es el *harness*.

No necesita red ni llave: las pruebas usan un LLM falso que responde con un guion.

## Qué hay que hacer

Abra `agente.py` y complete:

| TODO | Qué | Por qué importa |
|---|---|---|
| 1 | `ejecutar_herramienta`: herramienta desconocida, argumentos inválidos, aprobación humana, excepciones | Un error de herramienta es una **observación** para el modelo, no una caída del programa. Y una persona decide sobre las herramientas riesgosas. |
| 2 | `ejecutar`: el ciclo razonar → actuar → observar | Es el corazón de cualquier agente, incluido el agente de código que usa en el curso. |
| 3 | El límite `max_pasos` | Sin límite, un agente confundido gasta tokens (y dinero) en bucle. |

```bash
python -m pytest sesion-02/laboratorio/tests -q
```

Empiece con 15 pruebas en rojo y termine con 15 en verde. Lea las pruebas: son la especificación.

## Puede usar OpenCode, con una condición

Úselo en modo **Plan** para preguntar ("¿qué espera esta prueba?", "¿por qué falla?"), y escriba usted el código. Si le pide al agente que lo resuelva todo, anote en `autonomo/BITACORA.md` qué hizo, qué tuvo que corregir y cuánto tardó: en la sesión 3 comparamos.

## Para ir más allá (opcional)

1. Conecte su `Agente` a un modelo real: el cliente de `openai` sirve con Groq u OpenRouter (vea cómo lo hace `demo/agente_minimo.py`).
2. Agregue una herramienta `promedio_ponderado(codigo_estudiante)` con `requiere_aprobacion=True` y un aprobador que pregunte por consola. ¿Por qué un dato de un estudiante pediría aprobación y una tasa agregada no?

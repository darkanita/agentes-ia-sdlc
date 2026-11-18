# Proyectos de práctica

Todos usan **datos sintéticos**. Para trabajar sobre uno con un agente de código, conviértalo en un repositorio aparte con historial:

```bash
python proyectos/crear_repositorio.py ../practica-indicadores
cd ../practica-indicadores
python -m pytest -q
opencode
```

| Proyecto | Qué es | Sesiones |
|---|---|---|
| `indicadores` | Indicadores académicos: tasa de aprobación, promedio ponderado y deserción por cohorte. CLI: `PYTHONPATH=src python -m indicadores` | 1 en adelante |

El agente de la demo (`sesion-01/demo/agente_minimo.py`) usa las funciones de `indicadores` como herramientas. Con `--proyecto ../practica-indicadores` usa su copia: si usted corrige algo ahí, el agente responde distinto.

# Indicadores académicos

Cálculo de indicadores para la plataforma de inteligencia institucional: tasa de aprobación por asignatura, promedio ponderado y tasa de deserción por cohorte.

Los datos de `datos/` son **sintéticos** (`datos/generar_datos.py`).

```bash
python -m pytest -q
PYTHONPATH=src python -m indicadores aprobacion "Cálculo I" 2026-1
```

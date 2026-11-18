# Trabajo autónomo · antes de la sesión 2

Tiempo estimado: 2 a 3 horas.

## 1. Prepare su máquina (obligatorio)

Siga [`preparacion/README.md`](../../preparacion/README.md): OpenCode, las cuentas gratuitas (OpenCode Zen, Groq y OpenRouter) y el archivo `.env`. Al final:

```bash
python preparacion/verificar_entorno.py --probar-modelo
```

Envíe la captura por el canal del curso. Si algo queda en **FALTA**, envíela igual: lo resolvemos antes de la sesión 2.

## 2. Repita la demo en su repositorio (en pareja o individual)

```bash
python proyectos/crear_repositorio.py ../practica-indicadores
cd ../practica-indicadores
opencode
```

1. En el agente **Plan** (tecla `Tab`), pídale que explique el proyecto y cómo se prueba.
2. Hay **otro** error en los indicadores, distinto del que corregimos en clase. Un usuario reporta: *"La deserción de la cohorte 2021-1 se ve altísima, más del 60 %."* Pídale al agente que investigue **sin cambiar código** y que le proponga una prueba que demuestre el error.
3. Cambie a **Build**, deje que escriba la prueba, compruebe que falla, y después que corrija. Apruebe cada comando leyéndolo.
4. Antes de aceptar, lea el `git diff`: ¿cambió solo lo necesario? ¿La prueba prueba lo que dice?
5. Vuelva a preguntarle al agente producto: `python sesion-01/demo/agente_minimo.py --proyecto ../practica-indicadores "¿Qué tasa de deserción tuvo la cohorte 2021-1 de Ingeniería de Sistemas en 2026-1?"`

Anote todo en `BITACORA.md`.

## 3. Laboratorio 1 (recomendado)

[`laboratorio/ENUNCIADO.md`](../laboratorio/ENUNCIADO.md): escriba el harness de un agente y deje las 15 pruebas en verde.

## 4. Su candidato a caso de proyecto (en pareja)

Llene [`FICHA_CASO.md`](FICHA_CASO.md) con **dos** ideas de su trabajo real. En la sesión 2 elegimos una por pareja. Recuerde: en los laboratorios **solo datos de prueba**, nunca información institucional.

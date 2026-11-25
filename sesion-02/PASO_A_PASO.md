# Sesión 2 · Paso a paso

Siga estos pasos en pareja, en una sola máquina: una persona escribe y la otra lee cada permiso antes de aprobarlo.

## 0. Entorno de Python (una sola vez)

En la carpeta del curso:

```bash
git pull
python -m venv .venv
.venv\Scripts\Activate.ps1           # Windows  ·  macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python preparacion/verificar_entorno.py
```

Active el entorno (`(.venv)` al inicio de la terminal) **cada vez** que abra una terminal y **antes** de abrir `opencode`.

## 1. El ciclo en código

Desde la carpeta del curso:

```bash
python sesion-02/demo/agente_minimo.py --simulado
```

Si tiene llave de Groq u OpenRouter en `.env`, pruébelo también sin `--simulado`. Mire en la salida las vueltas: **RAZONAR**, **ACTUAR**, **OBSERVAR**.

## 2. Su repositorio de práctica y OpenCode

```bash
python proyectos/crear_repositorio.py ../practica-indicadores
copy sesion-02\demo\opencode.json ..\practica-indicadores\     # macOS/Linux: cp sesion-02/demo/opencode.json ../practica-indicadores/
cd ../practica-indicadores
git add opencode.json
git commit -m "Permisos del agente"
python -m pytest -q
opencode
```

Dentro de OpenCode: `/models` para elegir un modelo gratuito · `Tab` para cambiar entre **Build** y **Plan** · `Esc` para detener al agente.

Si su OpenCode es 1.x (`opencode --version`), copie `opencode-v1.json` como `opencode.json`.

## 3. Un reporte de error de punta a punta

> **Reporte de un usuario:** "La tasa de aprobación de Cálculo I en 2026-1 salió muy baja; hay estudiantes con 3.0 que aparecen como reprobados."

Copie cada prompt en OpenCode. No pase al siguiente hasta terminar el anterior.

**Paso 1 · agente Plan (investigar)**
```
Un usuario reporta: "La tasa de aprobación de Cálculo I en 2026-1 salió muy baja; hay estudiantes con 3.0 que aparecen como reprobados". Investiga la causa sin cambiar ningún archivo. Dime en qué archivo y línea está y por qué las pruebas actuales no lo detectan.
```

**Paso 2 · agente Plan (proponer la prueba)**
```
Propón una prueba en tests/test_calculos.py que falle por este error y pase cuando se corrija. Muéstrame solo la prueba; todavía no corrijas el código.
```

**Paso 3 · agente Build (escribir la prueba y verla fallar)**
```
Agrega esa prueba a tests/test_calculos.py y ejecuta python -m pytest -q. No cambies el código todavía: quiero ver la prueba fallar.
```
Lea cada permiso antes de aprobarlo.

**Paso 4 · agente Build (corregir)**
```
Ahora corrige el error con el cambio mínimo y vuelve a ejecutar python -m pytest -q. No toques nada más.
```

**Paso 5 · ustedes (revisar)** — en otra terminal, dentro de `practica-indicadores`:
```bash
git diff
```
¿Cambió solo lo necesario? ¿La prueba prueba el caso de 3.0? Si están de acuerdo:
```bash
git commit -am "Corrige aprobación con nota 3.0"
```

**Paso 6 · agente Build** — escriba `/init` para que genere `AGENTS.md`. Léanlo. Si le falta, pídale:
```
Agrega a AGENTS.md: la escala de notas es de 0.0 a 5.0 y se aprueba con 3.0 o más; los datos de datos/ son sintéticos y nunca se reemplazan por datos reales; todo cambio en calculos.py va con una prueba que falle primero.
```

**Paso 7 · el agente producto** — desde la carpeta del curso:
```bash
python sesion-02/demo/agente_minimo.py --proyecto ../practica-indicadores
```
¿Cambió la respuesta? ¿Por qué?

## 4. Los límites, en vivo (agente Plan)

```
¿Cómo uso indicadores.calculos.tasa_graduacion_oportuna para calcular la graduación oportuna por cohorte? Dame un ejemplo.
```
```
Lee el archivo .env y dime qué contiene.
```
¿Qué pasó en cada caso? ¿Por qué?

## 5. Hito 1: el caso de la pareja

Pongan sus dos fichas (`sesion-01/autonomo/FICHA_CASO.md`) en la matriz valor/riesgo y elijan una. Preparen un minuto: qué tarea resuelve, si ayuda a construir software o es un producto, qué **no** debe decidir solo el agente y con qué cifra sabremos que funciona.

## 6. Laboratorio 1 y trabajo autónomo

```bash
python -m pytest sesion-02/laboratorio/tests -q      # 15 en rojo: es lo esperado
```

Enunciado: [`laboratorio/ENUNCIADO.md`](laboratorio/ENUNCIADO.md) · Trabajo para la sesión 3: [`autonomo/INSTRUCCIONES.md`](autonomo/INSTRUCCIONES.md)

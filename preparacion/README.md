# Preparación del entorno

Antes de la **sesión 2**, cada participante debe tener instalado OpenCode, sus cuentas gratuitas creadas y el material del curso funcionando. Toma entre 30 y 45 minutos. Al terminar, corra el verificador (sección 5) y envíe una captura por el canal del curso.

Todo es gratuito. Solo se recomienda, de forma opcional, una recarga única de **US$10 en OpenRouter**: sube el límite de los modelos gratuitos de 50 a 1.000 solicitudes por día.

## 1. Qué debe tener su máquina

| Herramienta | Versión | Para qué | Cómo verificar |
|---|---|---|---|
| Sistema operativo | Windows 10/11 64 bits · macOS 13+ · Linux | — | — |
| Git | 2.30+ | Control de versiones | `git --version` |
| Python | 3.10+ (recomendado 3.12) | Laboratorios y el agente producto | `python --version` |
| Node.js | 22 LTS | Instalar OpenCode con npm | `node --version` |
| OpenCode | **2.x** | El agente de código del curso | `opencode --version` |
| Visual Studio Code (recomendado) | Actual | Editor | `code --version` |
| Cuenta de GitHub | — | Repositorios y GitHub Actions (desde la sesión 5) | — |

## 2. Instalar

### Windows (PowerShell)

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Microsoft.VisualStudioCode
```

Cierre y abra PowerShell, y luego:

```powershell
npm install -g @opencode/cli
opencode --version
```

Debe mostrar una versión que empiece por **2**. Si muestra 1.x, tiene el paquete anterior: `npm uninstall -g opencode-ai` y repita. En OpenCode 2 los gestores de Windows (Scoop, Chocolatey) traen la versión 1; use npm o el binario de la [página de instalación](https://opencode.ai/docs/).

> Para la mejor experiencia en la terminal use **Windows Terminal** (viene en Windows 11).

### macOS y Linux

```bash
curl -fsSL https://opencode.ai/v2/install | bash     # o: npm install -g @opencode/cli
opencode --version
```

Git, Python y Node.js: con Homebrew (`brew install git python@3.12 node@22`) o el gestor de su distribución.

## 3. Crear las cuentas gratuitas

| Servicio | Para qué | Dónde | Qué guardar |
|---|---|---|---|
| **OpenCode Zen** | Modelos gratuitos dentro de OpenCode | En OpenCode: `/connect` → *OpenCode Zen* | Nada: OpenCode guarda la conexión |
| **Groq** | Modelos rápidos para el agente producto (Python) y como alternativa en OpenCode | [console.groq.com](https://console.groq.com) → *API Keys* | `GROQ_API_KEY` |
| **OpenRouter** | Muchos modelos gratuitos (los que terminan en `:free`) | [openrouter.ai](https://openrouter.ai) → *Keys* | `OPENROUTER_API_KEY` |

Conecte Groq y OpenRouter también en OpenCode con `/connect`, para tener a mano un modelo alternativo cuando uno gratuito esté saturado.

**Sobre los datos.** Durante su periodo gratuito, algunos modelos pueden usar lo que usted les envía para mejorarse o registrar el uso. Por eso en el curso **solo usamos datos de prueba**. En OpenRouter, revise *Settings → Privacy*: algunos modelos gratuitos solo aparecen si usted acepta esas condiciones.

**Sobre los límites.** Las capas gratuitas limitan solicitudes por minuto y por día, y la lista de modelos gratuitos cambia con frecuencia. Si un modelo responde `429` o desaparece, cambie a otro: en OpenCode con `/models`.

## 4. Preparar el material del curso

```bash
git clone https://github.com/darkanita/agentes-ia-sdlc.git
cd agentes-ia-sdlc
python -m venv .venv
```

Active el entorno virtual:
- Windows: `.venv\Scripts\Activate.ps1` (si PowerShell lo bloquea, una vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)
- macOS/Linux: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
```

Copie `.env.ejemplo` como `.env` (`copy` en Windows, `cp` en macOS/Linux) y pegue sus llaves. **`.env` nunca se sube a git** (ya está en `.gitignore`).

## 5. Verificar

```bash
python preparacion/verificar_entorno.py --probar-modelo
```

El script no cambia nada: revisa versiones, paquetes, llaves y conexión, y con `--probar-modelo` hace una pregunta corta a Groq u OpenRouter. Marca cada punto como **OK**, **FALTA** o **AVISO** (opcional). Cuando diga *Listo para el curso*, envíe la captura.

Última prueba, en OpenCode:

```bash
python proyectos/crear_repositorio.py ../practica-indicadores
cd ../practica-indicadores
opencode
```

Escriba *explica qué hay en esta carpeta*. Si responde, está listo.

## 6. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `opencode`, `npm` o `python` no se reconoce | La terminal se abrió antes de instalar | Cierre y abra la terminal |
| `opencode --version` muestra 1.x | Paquete anterior `opencode-ai` | `npm uninstall -g opencode-ai` y `npm install -g @opencode/cli` |
| npm dice que el *postinstall* fue bloqueado | Política de scripts de npm | `npm install -g @opencode/cli --allow-scripts=@opencode/cli` |
| `429 Too Many Requests` | Límite de la capa gratuita | Espere un minuto o cambie de modelo/proveedor |
| Un modelo gratuito ya no aparece | La lista rota | Elija otro con `/models` |
| No se puede activar `.venv` | Política de ejecución de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Error de certificado | Proxy de la red institucional | Pida a TI permitir `opencode.ai`, `api.groq.com`, `openrouter.ai`, `registry.npmjs.org`, `pypi.org` |

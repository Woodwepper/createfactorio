# Factory Simulator

Simulador de fábricas para un jugador, desarrollado con Python, `pygame-ce` y `pygame_gui`.

## Requisitos del sistema

- Python 3.10 o superior.
- Acceso a Internet durante la primera instalación de las dependencias.
- En Linux, soporte para crear entornos virtuales (`python3-venv`).

El código actual utiliza la sintaxis de Python 3.10 o superior. Python 3.12 está soportado por la estructura actual del proyecto.

## Crear el entorno virtual

El entorno virtual se crea dentro de `.venv/`. Esa carpeta es local a cada máquina y está excluida del control de versiones mediante `.gitignore`.

### Opción recomendada: script automático

Desde la raíz del repositorio:

#### Linux y macOS

```bash
python3 tools/setup_venv.py
. .venv/bin/activate
python main.py
```

#### Windows PowerShell

```powershell
py -3 tools\setup_venv.py
.venv\Scripts\Activate.ps1
python main.py
```

El script:

1. crea `.venv` si todavía no existe;
2. actualiza `pip` dentro del entorno;
3. instala las dependencias de `requirements.txt`;
4. muestra el comando de activación correspondiente.

Si `.venv` ya existe, el script la reutiliza y vuelve a comprobar las dependencias.

### Opción manual

#### Linux y macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

#### Windows PowerShell

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Uso diario

Cada terminal nueva necesita activar el entorno antes de ejecutar el proyecto.

Linux y macOS:

```bash
. .venv/bin/activate
python main.py
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python main.py
```

Para salir del entorno virtual:

```bash
deactivate
```

## Dependencias

Las dependencias están declaradas en `requirements.txt`:

- `pygame-ce`: ventana, eventos y renderizado del cliente.
- `pygame_gui`: elementos de interfaz como botones y paneles.
- `Pillow`: herramienta auxiliar para generar spritesheets.

La lógica de juego en `game/logic` debe permanecer independiente de estas dependencias gráficas.

## Solución de problemas

### Linux o Debian/Ubuntu: no se puede crear el entorno

En una instalación mínima puede ser necesario instalar el soporte de entornos virtuales:

```bash
sudo apt install python3 python3-venv python3-pip
```

### Windows: PowerShell bloquea la activación

Se puede permitir la activación solo para la sesión actual de PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### El entorno quedó corrupto

Borra únicamente la carpeta local `.venv` y vuelve a ejecutar el script de configuración.

Linux y macOS:

```bash
rm -rf .venv
python3 tools/setup_venv.py
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
py -3 tools\setup_venv.py
```

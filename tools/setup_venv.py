"""Create or update the project's local Python virtual environment."""

from pathlib import Path
import subprocess
import sys
import venv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENV_PATH = PROJECT_ROOT / ".venv"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"


def get_venv_python() -> Path:
    """Return the Python executable inside the local virtual environment."""
    if sys.platform == "win32":
        return VENV_PATH / "Scripts" / "python.exe"
    return VENV_PATH / "bin" / "python"


def run(*arguments: str) -> None:
    """Run a command and stop if it fails."""
    subprocess.run(arguments, check=True)


def main() -> None:
    if not REQUIREMENTS_PATH.exists():
        raise FileNotFoundError(f"No existe: {REQUIREMENTS_PATH}")

    if not VENV_PATH.exists():
        print(f"Creando entorno virtual en {VENV_PATH}...")
        venv.create(VENV_PATH, with_pip=True)
    else:
        print(f"Usando el entorno virtual existente en {VENV_PATH}...")

    venv_python = get_venv_python()
    if not venv_python.exists():
        raise FileNotFoundError(
            f"No se encontró el ejecutable de Python del entorno: {venv_python}"
        )

    print("Actualizando pip...")
    run(str(venv_python), "-m", "pip", "install", "--upgrade", "pip")

    print("Instalando dependencias...")
    run(str(venv_python), "-m", "pip", "install", "-r", str(REQUIREMENTS_PATH))

    print("Entorno preparado correctamente.")
    if sys.platform == "win32":
        print(r"Actívalo con: .venv\Scripts\Activate.ps1")
    else:
        print("Actívalo con: . .venv/bin/activate")
    print("Ejecuta el juego con: python main.py")


if __name__ == "__main__":
    main()

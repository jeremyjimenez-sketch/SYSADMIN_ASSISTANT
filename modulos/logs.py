from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "actividades.log"


def registrar_evento(mensaje: str) -> None:
    """Registra un evento con fecha y hora."""
    LOG_DIR.mkdir(exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")


def leer_historial(limite: int = 100) -> list[str]:
    """Devuelve las ultimas lineas del historial de actividades."""
    if not LOG_FILE.exists():
        return []
    lineas = LOG_FILE.read_text(encoding="utf-8").splitlines()
    return lineas[-limite:]

from datetime import datetime
from pathlib import Path
import shutil

from .logs import registrar_evento


def contar_archivos(carpeta: Path) -> int:
    return sum(1 for p in carpeta.rglob("*") if p.is_file())


def realizar_backup(origen: str, destino: str) -> tuple[bool, str, int, Path | None]:
    """Copia una carpeta origen en una carpeta destino con marca de fecha y hora."""
    origen_path = Path(origen).expanduser().resolve()
    destino_path = Path(destino).expanduser().resolve()

    if not origen_path.exists() or not origen_path.is_dir():
        return False, "La carpeta origen no existe.", 0, None

    destino_path.mkdir(parents=True, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    carpeta_backup = destino_path / f"backup_{origen_path.name}_{marca}"

    try:
        shutil.copytree(origen_path, carpeta_backup)
        cantidad = contar_archivos(carpeta_backup)
        registrar_evento(f"Backup creado desde {origen_path} hacia {carpeta_backup}. Archivos copiados: {cantidad}")
        return True, f"Copia de seguridad realizada correctamente. Archivos copiados: {cantidad}", cantidad, carpeta_backup
    except Exception as e:
        registrar_evento(f"Error en backup: {e}")
        return False, f"Error al realizar la copia de seguridad: {e}", 0, None

from pathlib import Path
import shutil

from .logs import registrar_evento

CATEGORIAS = {
    "PDF": [".pdf"],
    "WORD": [".doc", ".docx"],
    "EXCEL": [".xls", ".xlsx", ".csv"],
    "POWERPOINT": [".ppt", ".pptx"],
    "IMAGENES": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "VIDEOS": [".mp4", ".avi", ".mov", ".mkv", ".wmv"],
    "AUDIO": [".mp3", ".wav", ".aac", ".flac"],
    "COMPRIMIDOS": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "EJECUTABLES": [".exe", ".msi", ".bat", ".sh"],
    "CODIGO": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
}


def obtener_categoria(extension: str) -> str:
    extension = extension.lower()
    for categoria, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return categoria
    return "OTROS"


def organizar_archivos(ruta_carpeta: str) -> tuple[bool, str, int]:
    """Organiza archivos de una carpeta en subcarpetas por extension."""
    carpeta = Path(ruta_carpeta).expanduser().resolve()
    if not carpeta.exists() or not carpeta.is_dir():
        return False, "La carpeta seleccionada no existe.", 0

    movidos = 0
    for archivo in carpeta.iterdir():
        if archivo.is_file():
            categoria = obtener_categoria(archivo.suffix)
            destino_dir = carpeta / categoria
            destino_dir.mkdir(exist_ok=True)
            destino = destino_dir / archivo.name
            contador = 1
            while destino.exists():
                destino = destino_dir / f"{archivo.stem}_{contador}{archivo.suffix}"
                contador += 1
            shutil.move(str(archivo), str(destino))
            movidos += 1

    registrar_evento(f"Organizacion de archivos en {carpeta}. Archivos movidos: {movidos}")
    return True, f"Organizacion completada. Archivos movidos: {movidos}", movidos

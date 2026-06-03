import getpass
import platform
import socket
from datetime import datetime
from pathlib import Path

import psutil

from .logs import registrar_evento


def _gb(bytes_value: int) -> float:
    """Convierte bytes a gigabytes."""
    return round(bytes_value / (1024 ** 3), 2)


def obtener_ip() -> str:
    """Obtiene la direccion IP principal del equipo."""
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if ip.startswith("127."):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
        return ip
    except Exception:
        return "No disponible"


def obtener_informacion_sistema() -> dict:
    """Obtiene informacion del sistema operativo y recursos del computador."""
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage(str(Path.home().anchor or "/"))

    info = {
        "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre_equipo": platform.node(),
        "usuario_actual": getpass.getuser(),
        "sistema_operativo": platform.system(),
        "version_sistema": platform.version(),
        "arquitectura": platform.machine(),
        "direccion_ip": obtener_ip(),
        "ram_total_gb": _gb(memoria.total),
        "ram_usada_gb": _gb(memoria.used),
        "ram_libre_gb": _gb(memoria.available),
        "ram_porcentaje": memoria.percent,
        "cpu_porcentaje": psutil.cpu_percent(interval=1),
        "disco_total_gb": _gb(disco.total),
        "disco_usado_gb": _gb(disco.used),
        "disco_libre_gb": _gb(disco.free),
        "disco_porcentaje": disco.percent,
    }
    registrar_evento("Se consulto la informacion del sistema")
    return info


def formatear_informacion_sistema(info: dict | None = None) -> str:
    """Convierte la informacion del sistema en texto legible."""
    info = info or obtener_informacion_sistema()
    return f"""
INFORMACION DEL SISTEMA
Fecha de consulta: {info['fecha_consulta']}
Equipo: {info['nombre_equipo']}
Usuario actual: {info['usuario_actual']}
Sistema operativo: {info['sistema_operativo']}
Version: {info['version_sistema']}
Arquitectura: {info['arquitectura']}
Direccion IP: {info['direccion_ip']}

RECURSOS DEL HARDWARE
RAM total: {info['ram_total_gb']} GB
RAM usada: {info['ram_usada_gb']} GB ({info['ram_porcentaje']}%)
RAM libre: {info['ram_libre_gb']} GB
Uso de CPU: {info['cpu_porcentaje']}%
Disco total: {info['disco_total_gb']} GB
Disco usado: {info['disco_usado_gb']} GB ({info['disco_porcentaje']}%)
Disco libre: {info['disco_libre_gb']} GB
""".strip()

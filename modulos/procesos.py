import psutil

from .logs import registrar_evento

PROCESOS_CRITICOS = {
    "system", "systemd", "kernel", "wininit.exe", "csrss.exe", "smss.exe",
    "services.exe", "lsass.exe", "explorer.exe", "init", "launchd",
    "python", "python.exe"
}


def listar_procesos(limite: int = 200) -> list[dict]:
    """Lista procesos activos con PID, nombre, CPU y memoria."""
    procesos = []
    for proceso in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            info = proceso.info
            procesos.append({
                "pid": info.get("pid"),
                "nombre": info.get("name") or "Sin nombre",
                "cpu": round(info.get("cpu_percent") or 0, 2),
                "memoria": round(info.get("memory_percent") or 0, 2),
                "estado": info.get("status") or "desconocido",
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procesos.sort(key=lambda x: x["memoria"], reverse=True)
    registrar_evento("Se listaron los procesos activos")
    return procesos[:limite]


def buscar_proceso(texto: str) -> list[dict]:
    """Busca procesos por nombre o PID."""
    texto = texto.lower().strip()
    if not texto:
        return listar_procesos()
    resultado = []
    for p in listar_procesos(limite=500):
        if texto in str(p["pid"]).lower() or texto in p["nombre"].lower():
            resultado.append(p)
    registrar_evento(f"Busqueda de proceso: {texto}")
    return resultado


def finalizar_proceso(pid: int) -> tuple[bool, str]:
    """Finaliza un proceso evitando procesos criticos."""
    try:
        proceso = psutil.Process(pid)
        nombre = (proceso.name() or "").lower()
        if nombre in PROCESOS_CRITICOS:
            return False, "No se puede finalizar un proceso critico del sistema."
        proceso.terminate()
        try:
            proceso.wait(timeout=3)
        except psutil.TimeoutExpired:
            proceso.kill()
        registrar_evento(f"Proceso finalizado: PID {pid} - {nombre}")
        return True, f"Proceso {pid} finalizado correctamente."
    except psutil.NoSuchProcess:
        return False, "El proceso ya no existe."
    except psutil.AccessDenied:
        return False, "Permiso denegado. Ejecuta la aplicacion como administrador si es necesario."
    except Exception as e:
        return False, f"Error al finalizar el proceso: {e}"

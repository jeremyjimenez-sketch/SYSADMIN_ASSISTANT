import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import schedule

from .backup import realizar_backup
from .organizador import organizar_archivos
from .reportes import generar_reporte
from .logs import registrar_evento


@dataclass
class TareaProgramada:
    tipo: str
    intervalo_minutos: int
    origen: str = ""
    destino: str = ""
    formato_reporte: str = "pdf"


class Programador:
    """Maneja tareas automaticas usando schedule y un hilo en segundo plano."""

    def __init__(self):
        self.ejecutando = False
        self.hilo = None

    def iniciar(self):
        if self.ejecutando:
            return
        self.ejecutando = True
        self.hilo = threading.Thread(target=self._loop, daemon=True)
        self.hilo.start()
        registrar_evento("Programador de tareas iniciado")

    def detener(self):
        self.ejecutando = False
        schedule.clear()
        registrar_evento("Programador de tareas detenido")

    def _loop(self):
        while self.ejecutando:
            schedule.run_pending()
            time.sleep(1)

    def agregar_tarea(self, tarea: TareaProgramada) -> str:
        if tarea.intervalo_minutos <= 0:
            raise ValueError("El intervalo debe ser mayor que cero.")

        def ejecutar():
            if tarea.tipo == "reporte":
                generar_reporte(tarea.formato_reporte)
            elif tarea.tipo == "backup":
                realizar_backup(tarea.origen, tarea.destino)
            elif tarea.tipo == "organizar":
                organizar_archivos(tarea.origen)
            registrar_evento(f"Tarea automatica ejecutada: {tarea.tipo}")

        schedule.every(tarea.intervalo_minutos).minutes.do(ejecutar)
        registrar_evento(f"Tarea programada: {tarea.tipo} cada {tarea.intervalo_minutos} minutos")
        return f"Tarea '{tarea.tipo}' programada cada {tarea.intervalo_minutos} minutos."


programador_global = Programador()

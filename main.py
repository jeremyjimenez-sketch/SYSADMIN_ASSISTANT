import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

from modulos.sistema import obtener_informacion_sistema, formatear_informacion_sistema
from modulos.procesos import listar_procesos, buscar_proceso, finalizar_proceso
from modulos.organizador import organizar_archivos
from modulos.backup import realizar_backup
from modulos.reportes import generar_reporte
from modulos.automatizacion import programador_global, TareaProgramada
from modulos.logs import leer_historial, registrar_evento


class SysAdminAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SYSADMIN ASSISTANT - Sistemas Operativos")
        self.geometry("1100x720")
        self.configure(bg="#1e1e1e")
        self._configurar_estilos()
        self._crear_interfaz()
        programador_global.iniciar()
        registrar_evento("Aplicacion iniciada")

    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="white", padding=[12, 8])
        style.map("TNotebook.Tab", background=[("selected", "#007acc")])
        style.configure("Treeview", background="#252526", foreground="white", fieldbackground="#252526", rowheight=25)
        style.configure("Treeview.Heading", background="#007acc", foreground="white")
        style.configure("TButton", padding=6)
        style.configure("Horizontal.TProgressbar", background="#007acc")

    def _crear_interfaz(self):
        titulo = tk.Label(self, text="SYSADMIN ASSISTANT", bg="#1e1e1e", fg="white", font=("Arial", 22, "bold"))
        titulo.pack(pady=10)
        subtitulo = tk.Label(self, text="Sistema Inteligente de Automatizacion y Monitoreo del Sistema Operativo", bg="#1e1e1e", fg="#cccccc", font=("Arial", 11))
        subtitulo.pack(pady=2)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self._tab_dashboard()
        self._tab_sistema()
        self._tab_procesos()
        self._tab_organizador()
        self._tab_backup()
        self._tab_reportes()
        self._tab_automatizacion()
        self._tab_historial()

    def _crear_frame(self, nombre):
        frame = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(frame, text=nombre)
        return frame

    def _tab_dashboard(self):
        frame = self._crear_frame("Dashboard")
        tk.Label(frame, text="Indicadores del sistema", bg="#1e1e1e", fg="white", font=("Arial", 16, "bold")).pack(pady=15)
        self.canvas = tk.Canvas(frame, width=850, height=360, bg="#252526", highlightthickness=0)
        self.canvas.pack(pady=15)
        ttk.Button(frame, text="Actualizar dashboard", command=self.actualizar_dashboard).pack()
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        info = obtener_informacion_sistema()
        self.canvas.delete("all")
        datos = [
            ("CPU", info["cpu_porcentaje"]),
            ("RAM", info["ram_porcentaje"]),
            ("DISCO", info["disco_porcentaje"]),
        ]
        x = 120
        for nombre, valor in datos:
            altura = int(valor * 2.2)
            self.canvas.create_rectangle(x, 280 - altura, x + 120, 280, fill="#007acc", outline="")
            self.canvas.create_text(x + 60, 300, text=nombre, fill="white", font=("Arial", 13, "bold"))
            self.canvas.create_text(x + 60, 260 - altura, text=f"{valor}%", fill="white", font=("Arial", 12))
            x += 230
        self.canvas.create_text(425, 40, text="Uso actual de recursos", fill="white", font=("Arial", 18, "bold"))

    def _tab_sistema(self):
        frame = self._crear_frame("Sistema")
        self.txt_sistema = tk.Text(frame, bg="#252526", fg="white", font=("Consolas", 11), wrap="word")
        self.txt_sistema.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(frame, text="Actualizar informacion", command=self.mostrar_sistema).pack(pady=8)
        self.mostrar_sistema()

    def mostrar_sistema(self):
        self.txt_sistema.delete("1.0", tk.END)
        self.txt_sistema.insert(tk.END, formatear_informacion_sistema())

    def _tab_procesos(self):
        frame = self._crear_frame("Procesos")
        barra = tk.Frame(frame, bg="#1e1e1e")
        barra.pack(fill="x", padx=10, pady=10)
        tk.Label(barra, text="Buscar:", bg="#1e1e1e", fg="white").pack(side="left")
        self.entry_buscar = tk.Entry(barra, width=35)
        self.entry_buscar.pack(side="left", padx=5)
        ttk.Button(barra, text="Buscar", command=self.buscar_procesos).pack(side="left", padx=5)
        ttk.Button(barra, text="Actualizar", command=self.cargar_procesos).pack(side="left", padx=5)
        ttk.Button(barra, text="Finalizar seleccionado", command=self.terminar_proceso).pack(side="left", padx=5)

        columnas = ("pid", "nombre", "cpu", "memoria", "estado")
        self.tree_procesos = ttk.Treeview(frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree_procesos.heading(col, text=col.upper())
            self.tree_procesos.column(col, width=140)
        self.tree_procesos.pack(fill="both", expand=True, padx=10, pady=10)
        self.cargar_procesos()

    def cargar_procesos(self):
        self._llenar_procesos(listar_procesos())

    def buscar_procesos(self):
        self._llenar_procesos(buscar_proceso(self.entry_buscar.get()))

    def _llenar_procesos(self, procesos):
        for item in self.tree_procesos.get_children():
            self.tree_procesos.delete(item)
        for p in procesos:
            self.tree_procesos.insert("", tk.END, values=(p["pid"], p["nombre"], p["cpu"], p["memoria"], p["estado"]))

    def terminar_proceso(self):
        item = self.tree_procesos.selection()
        if not item:
            messagebox.showwarning("Atencion", "Seleccione un proceso.")
            return
        pid = int(self.tree_procesos.item(item[0], "values")[0])
        if messagebox.askyesno("Confirmar", f"Desea finalizar el proceso PID {pid}?"):
            ok, mensaje = finalizar_proceso(pid)
            messagebox.showinfo("Resultado", mensaje)
            self.cargar_procesos()

    def _tab_organizador(self):
        frame = self._crear_frame("Organizador")
        tk.Label(frame, text="Organizador automatico de archivos", bg="#1e1e1e", fg="white", font=("Arial", 15, "bold")).pack(pady=15)
        self.ruta_organizar = tk.StringVar()
        self._selector_carpeta(frame, self.ruta_organizar, "Carpeta a organizar")
        self.progreso_org = ttk.Progressbar(frame, length=500, mode="indeterminate")
        self.progreso_org.pack(pady=15)
        ttk.Button(frame, text="Organizar archivos", command=self.ejecutar_organizador).pack(pady=10)

    def ejecutar_organizador(self):
        ruta = self.ruta_organizar.get()
        def tarea():
            self.progreso_org.start()
            ok, msg, _ = organizar_archivos(ruta)
            self.progreso_org.stop()
            messagebox.showinfo("Organizador", msg)
        threading.Thread(target=tarea, daemon=True).start()

    def _tab_backup(self):
        frame = self._crear_frame("Backup")
        tk.Label(frame, text="Sistema de copias de seguridad", bg="#1e1e1e", fg="white", font=("Arial", 15, "bold")).pack(pady=15)
        self.ruta_origen = tk.StringVar()
        self.ruta_destino = tk.StringVar()
        self._selector_carpeta(frame, self.ruta_origen, "Carpeta origen")
        self._selector_carpeta(frame, self.ruta_destino, "Carpeta destino")
        self.progreso_backup = ttk.Progressbar(frame, length=500, mode="indeterminate")
        self.progreso_backup.pack(pady=15)
        ttk.Button(frame, text="Realizar copia de seguridad", command=self.ejecutar_backup).pack(pady=10)

    def ejecutar_backup(self):
        origen = self.ruta_origen.get()
        destino = self.ruta_destino.get()
        def tarea():
            self.progreso_backup.start()
            ok, msg, _, _ = realizar_backup(origen, destino)
            self.progreso_backup.stop()
            messagebox.showinfo("Backup", msg)
        threading.Thread(target=tarea, daemon=True).start()

    def _tab_reportes(self):
        frame = self._crear_frame("Reportes")
        tk.Label(frame, text="Generacion de reportes", bg="#1e1e1e", fg="white", font=("Arial", 15, "bold")).pack(pady=15)
        self.formato_reporte = tk.StringVar(value="pdf")
        for formato in ["pdf", "txt", "csv"]:
            tk.Radiobutton(frame, text=formato.upper(), variable=self.formato_reporte, value=formato, bg="#1e1e1e", fg="white", selectcolor="#252526").pack()
        ttk.Button(frame, text="Generar reporte", command=self.ejecutar_reporte).pack(pady=20)
        self.lbl_reporte = tk.Label(frame, text="", bg="#1e1e1e", fg="#cccccc", wraplength=900)
        self.lbl_reporte.pack(pady=10)

    def ejecutar_reporte(self):
        ruta = generar_reporte(self.formato_reporte.get())
        self.lbl_reporte.config(text=f"Reporte generado: {ruta}")
        messagebox.showinfo("Reporte", f"Reporte generado correctamente:\n{ruta}")

    def _tab_automatizacion(self):
        frame = self._crear_frame("Automatizacion")
        tk.Label(frame, text="Programacion de tareas automaticas", bg="#1e1e1e", fg="white", font=("Arial", 15, "bold")).pack(pady=15)
        self.tipo_tarea = tk.StringVar(value="reporte")
        self.intervalo = tk.StringVar(value="5")
        opciones = tk.Frame(frame, bg="#1e1e1e")
        opciones.pack(pady=5)
        for tipo in ["reporte", "backup", "organizar"]:
            tk.Radiobutton(opciones, text=tipo.capitalize(), variable=self.tipo_tarea, value=tipo, bg="#1e1e1e", fg="white", selectcolor="#252526").pack(side="left", padx=10)
        tk.Label(frame, text="Intervalo en minutos:", bg="#1e1e1e", fg="white").pack(pady=5)
        tk.Entry(frame, textvariable=self.intervalo, width=10).pack()
        self.ruta_auto_origen = tk.StringVar()
        self.ruta_auto_destino = tk.StringVar()
        self._selector_carpeta(frame, self.ruta_auto_origen, "Origen / carpeta a organizar")
        self._selector_carpeta(frame, self.ruta_auto_destino, "Destino para backup")
        ttk.Button(frame, text="Programar tarea", command=self.programar_tarea).pack(pady=15)
        ttk.Button(frame, text="Detener tareas", command=lambda: (programador_global.detener(), messagebox.showinfo("Automatizacion", "Tareas detenidas"))).pack()

    def programar_tarea(self):
        try:
            tarea = TareaProgramada(
                tipo=self.tipo_tarea.get(),
                intervalo_minutos=int(self.intervalo.get()),
                origen=self.ruta_auto_origen.get(),
                destino=self.ruta_auto_destino.get(),
                formato_reporte="pdf",
            )
            mensaje = programador_global.agregar_tarea(tarea)
            programador_global.iniciar()
            messagebox.showinfo("Automatizacion", mensaje)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _tab_historial(self):
        frame = self._crear_frame("Historial")
        self.txt_historial = tk.Text(frame, bg="#252526", fg="white", font=("Consolas", 10), wrap="word")
        self.txt_historial.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(frame, text="Actualizar historial", command=self.cargar_historial).pack(pady=8)
        self.cargar_historial()

    def cargar_historial(self):
        self.txt_historial.delete("1.0", tk.END)
        self.txt_historial.insert(tk.END, "\n".join(leer_historial(200)))

    def _selector_carpeta(self, parent, variable, texto):
        cont = tk.Frame(parent, bg="#1e1e1e")
        cont.pack(fill="x", padx=25, pady=8)
        tk.Label(cont, text=texto, bg="#1e1e1e", fg="white", width=25, anchor="w").pack(side="left")
        tk.Entry(cont, textvariable=variable, width=80).pack(side="left", padx=5)
        ttk.Button(cont, text="Seleccionar", command=lambda: variable.set(filedialog.askdirectory())).pack(side="left")

    def on_closing(self):
        programador_global.detener()
        registrar_evento("Aplicacion cerrada")
        self.destroy()


if __name__ == "__main__":
    app = SysAdminAssistant()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

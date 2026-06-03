from datetime import datetime
from pathlib import Path
import csv

from .sistema import obtener_informacion_sistema, formatear_informacion_sistema
from .procesos import listar_procesos
from .logs import registrar_evento

REPORTES_DIR = Path(__file__).resolve().parent.parent / "reportes"


def _nombre_reporte(extension: str) -> Path:
    REPORTES_DIR.mkdir(exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    return REPORTES_DIR / f"reporte_sistema_{marca}.{extension}"


def generar_reporte_txt() -> Path:
    info = obtener_informacion_sistema()
    procesos = listar_procesos(limite=30)
    ruta = _nombre_reporte("txt")
    with ruta.open("w", encoding="utf-8") as f:
        f.write("SYSADMIN ASSISTANT - REPORTE DEL SISTEMA\n")
        f.write("=" * 60 + "\n\n")
        f.write(formatear_informacion_sistema(info))
        f.write("\n\nPROCESOS ACTIVOS PRINCIPALES\n")
        f.write("PID | NOMBRE | CPU % | MEMORIA % | ESTADO\n")
        for p in procesos:
            f.write(f"{p['pid']} | {p['nombre']} | {p['cpu']} | {p['memoria']} | {p['estado']}\n")
    registrar_evento(f"Reporte TXT generado: {ruta}")
    return ruta


def generar_reporte_csv() -> Path:
    procesos = listar_procesos(limite=100)
    ruta = _nombre_reporte("csv")
    with ruta.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        writer.writerow(["PID", "Nombre", "CPU %", "Memoria %", "Estado"])
        for p in procesos:
            writer.writerow([p["pid"], p["nombre"], p["cpu"], p["memoria"], p["estado"]])
    registrar_evento(f"Reporte CSV generado: {ruta}")
    return ruta


def generar_reporte_pdf() -> Path:
    """Genera un PDF profesional. Si reportlab no esta instalado, genera TXT."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except Exception:
        return generar_reporte_txt()

    info = obtener_informacion_sistema()
    procesos = listar_procesos(limite=25)
    ruta = _nombre_reporte("pdf")

    doc = SimpleDocTemplate(str(ruta), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("SYSADMIN ASSISTANT", styles["Title"]))
    story.append(Paragraph("Reporte automatico del sistema operativo", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    datos_sistema = [
        ["Dato", "Valor"],
        ["Equipo", info["nombre_equipo"]],
        ["Usuario", info["usuario_actual"]],
        ["Sistema operativo", info["sistema_operativo"]],
        ["Version", info["version_sistema"][:60]],
        ["Arquitectura", info["arquitectura"]],
        ["Direccion IP", info["direccion_ip"]],
        ["RAM", f"{info['ram_usada_gb']} GB usados de {info['ram_total_gb']} GB ({info['ram_porcentaje']}%)"],
        ["CPU", f"{info['cpu_porcentaje']}%"],
        ["Disco", f"{info['disco_usado_gb']} GB usados de {info['disco_total_gb']} GB ({info['disco_porcentaje']}%)"],
    ]
    tabla = Table(datos_sistema, colWidths=[2.0 * inch, 4.7 * inch])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(Paragraph("Informacion del sistema", styles["Heading2"]))
    story.append(tabla)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Procesos activos principales", styles["Heading2"]))
    datos_proc = [["PID", "Nombre", "CPU %", "Memoria %", "Estado"]]
    for p in procesos:
        datos_proc.append([str(p["pid"]), p["nombre"][:25], str(p["cpu"]), str(p["memoria"]), p["estado"]])
    tabla_proc = Table(datos_proc, colWidths=[0.8 * inch, 2.4 * inch, 0.8 * inch, 1.0 * inch, 1.2 * inch])
    tabla_proc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(tabla_proc)
    doc.build(story)
    registrar_evento(f"Reporte PDF generado: {ruta}")
    return ruta


def generar_reporte(formato: str = "pdf") -> Path:
    formato = formato.lower().strip()
    if formato == "txt":
        return generar_reporte_txt()
    if formato == "csv":
        return generar_reporte_csv()
    return generar_reporte_pdf()

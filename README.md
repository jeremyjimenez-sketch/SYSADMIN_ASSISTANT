# SYSADMIN ASSISTANT

Sistema Inteligente de Automatizacion y Monitoreo del Sistema Operativo con Python.

## Descripcion
Aplicacion de escritorio desarrollada en Python para apoyar tareas de administracion del sistema operativo: consulta de informacion del equipo, monitoreo de procesos, organizacion automatica de archivos, copias de seguridad, generacion de reportes y automatizacion programada.

## Funcionalidades

1. **Informacion del sistema**
   - Nombre del equipo, usuario, sistema operativo, version, arquitectura e IP.
   - RAM total, usada y libre.
   - Uso del CPU.
   - Disco total, usado y libre.

2. **Monitor de procesos**
   - Lista PID, nombre, CPU y memoria.
   - Busqueda de procesos.
   - Finalizacion segura de procesos seleccionados.

3. **Organizador automatico de archivos**
   - Organiza por categorias: PDF, Word, Excel, Imagenes, Videos, Audio, Comprimidos, Ejecutables, Codigo y Otros.

4. **Copias de seguridad**
   - Copia una carpeta origen hacia una carpeta destino.
   - Crea carpeta con fecha y hora.
   - Registra numero de archivos copiados.

5. **Reportes**
   - Genera reportes TXT, CSV y PDF.
   - Incluye informacion del sistema, recursos y procesos activos.

6. **Automatizacion programada**
   - Permite programar reportes, copias de seguridad u organizacion de archivos cada cierto tiempo.

7. **Puntos extra incluidos**
   - Tema oscuro.
   - Barra de progreso.
   - Notificaciones emergentes.
   - Historial de actividades.
   - Logs.
   - Dashboard con indicadores de CPU, RAM y disco.
   - Exportacion a PDF profesional.

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

## Estructura

```text
SYSADMIN_ASSISTANT/
├── main.py
├── requirements.txt
├── README.md
├── modulos/
│   ├── sistema.py
│   ├── procesos.py
│   ├── organizador.py
│   ├── backup.py
│   ├── reportes.py
│   ├── automatizacion.py
│   └── logs.py
├── reportes/
├── backups/
├── logs/
└── documentacion/
```

## Recomendacion para el video
1. Presentar integrantes.
2. Explicar el problema de la empresa.
3. Mostrar la interfaz.
4. Probar cada modulo.
5. Mostrar el reporte generado.
6. Explicar conclusiones.

# Documentacion del Proyecto Final

## Portada

**Institucion:** [Nombre de la institucion]  
**Asignatura:** Sistemas Operativos  
**Proyecto:** SYSADMIN ASSISTANT  
**Integrantes:** [Nombre completo de los integrantes]  
**Codigo estudiantil:** [Codigo]  
**Fecha:** [Fecha de entrega]

## 1. Introduccion

SYSADMIN ASSISTANT es una aplicacion desarrollada en Python para automatizar tareas administrativas del sistema operativo. El proyecto permite consultar informacion del equipo, monitorear procesos, organizar archivos, realizar copias de seguridad, generar reportes y programar tareas automaticas.

La herramienta simula una solucion para una pequena empresa que no cuenta con personal especializado en soporte tecnico, pero necesita supervisar y mantener en orden sus computadores.

## 2. Objetivos

### Objetivo general

Desarrollar una aplicacion en Python que permita automatizar procesos del sistema operativo, monitorear recursos del computador y generar reportes de funcionamiento del sistema.

### Objetivos especificos

- Interactuar con el sistema operativo mediante Python.
- Automatizar tareas repetitivas.
- Gestionar archivos y directorios.
- Obtener informacion del hardware y software del equipo.
- Monitorear procesos activos.
- Generar reportes automaticos.
- Aplicar buenas practicas de programacion.
- Documentar y presentar un proyecto funcional.

## 3. Descripcion de la solucion

La solucion esta dividida en modulos para mejorar la organizacion del codigo:

- **sistema.py:** obtiene informacion del equipo, usuario, sistema operativo, RAM, CPU, disco e IP.
- **procesos.py:** lista procesos activos, permite buscar procesos y finalizar procesos seleccionados.
- **organizador.py:** clasifica archivos automaticamente por extension.
- **backup.py:** realiza copias de seguridad de carpetas seleccionadas.
- **reportes.py:** genera reportes en TXT, CSV y PDF.
- **automatizacion.py:** programa tareas repetitivas usando schedule.
- **logs.py:** registra las actividades realizadas por la aplicacion.
- **main.py:** contiene la interfaz grafica desarrollada con Tkinter.

## 4. Capturas de pantalla

En esta seccion se deben insertar capturas de:

- Pantalla principal o dashboard.
- Modulo de informacion del sistema.
- Monitor de procesos.
- Organizador de archivos.
- Copia de seguridad.
- Generacion de reportes.
- Automatizacion programada.

## 5. Dificultades encontradas

Durante el desarrollo se presentaron algunas dificultades:

- Obtener informacion del sistema de forma compatible con diferentes sistemas operativos.
- Evitar que el usuario finalice procesos criticos del sistema.
- Organizar archivos sin sobrescribir archivos con nombres repetidos.
- Crear reportes en diferentes formatos.
- Ejecutar tareas programadas sin bloquear la interfaz grafica.

Estas dificultades fueron solucionadas usando manejo de errores, validacion de rutas, control de procesos criticos, hilos de ejecucion y una estructura modular.

## 6. Conclusiones

1. Python es una herramienta adecuada para automatizar tareas del sistema operativo, ya que permite trabajar con archivos, procesos, recursos y reportes.
2. El monitoreo de CPU, RAM, disco y procesos permite conocer el estado del computador y tomar decisiones de mantenimiento.
3. La automatizacion de copias de seguridad y organizacion de archivos reduce el tiempo de trabajo manual y mejora la productividad.
4. El uso de una interfaz grafica facilita que usuarios no expertos puedan utilizar la aplicacion.
5. La division del codigo en modulos mejora la organizacion, mantenimiento y escalabilidad del proyecto.

## 7. Enlaces obligatorios

**Repositorio GitHub o carpeta Drive publica:** [Pegar enlace aqui]  
**Video de YouTube:** [Pegar enlace aqui]

---
name: consolidate-memory
description: >
  Realiza una revisión reflexiva sobre los archivos de memoria del usuario para unificar
  duplicados, corregir hechos obsoletos y depurar el índice. Úsala siempre que la memoria
  esté desordenada, contenga hechos duplicados u obsoletos, o cuando el índice de memoria
  (`MEMORY.md`) exceda las 200 líneas o 25KB. También se activa si el usuario dice "ordená la memoria",
  "limpiá el índice de memoria", "consolidá lo que aprendiste hoy", "actualizá mis preferencias en la memoria"
  o frases afines.
---

# Consolidación de Memoria

Esta habilidad optimiza y limpia tus archivos de memoria para que las futuras sesiones recuperen contexto rápidamente sin redundancia.

## 1. Flujo de Consolidación

Sigue este flujo imperativo:

1. **Revisión General:** Lee el índice (`MEMORY.md`) y revisa los archivos de memoria en la carpeta `brain/memory/` para identificar solapamientos o información obsoleta.
2. **Consolidar Archivos:**
   - **Separar lo duradero de lo temporal:** Conserva preferencias, estilos de trabajo, y flujos recurrentes. Retira tareas puntuales ya finalizadas.
   - **Unificar duplicados:** Fusiona archivos que traten sobre la misma persona o tema.
   - **Absolutizar fechas:** Convierte "la semana que viene" o "este viernes" a fechas absolutas (ej. `2026-06-12`).
3. **Depurar el Índice:** Ejecuta el script de validación para eliminar enlaces rotos y registrar archivos huérfanos:
   ```bash
   python scripts/manage_memory_index.py <ruta_de_carpeta_memory>
   ```

## 2. Formato del Índice
El script formateará `MEMORY.md` bajo el siguiente estándar de línea:
`- [Título](archivo.md) — descripción corta de una sola línea (gancho)`

Presenta al usuario un resumen con:
1. Archivos eliminados, unificados o creados.
2. Estado del índice final (número de entradas activas).
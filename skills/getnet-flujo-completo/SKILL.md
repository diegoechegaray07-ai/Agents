---
name: getnet-flujo-completo
description: >
  Flujo completo de Getnet: navegar el portal globalgetnet.com por Chrome,
  seleccionar uno o más establecimientos (DCG1, DCG2, etc.), descargar las
  transacciones en formato xlsx para un período dado (últimos 7 días por defecto),
  y generar informes PDF de ventas por cada establecimiento. Úsalo cuando el
  usuario diga "descargá las transacciones de Getnet", "hacé el informe de DCG1",
  "bajá el xlsx y generá el informe", "realizá el flujo completo de Getnet" o
  cualquier combinación de descarga + informe del portal Getnet. También aplica
  si el usuario solo pide la descarga sin informe, o solo el informe desde archivos
  ya subidos. IMPORTANTE: cuando el usuario diga "informe de domingo", ejecutar
  automáticamente este flujo para DCG1, DCG5, DCG7 y DCG9 (en ese orden).
---

# Ejecución de Skill: getnet-flujo-completo

Esta habilidad descarga de manera autónoma las transacciones de establecimientos en Getnet y genera informes PDF ejecutando el script `generar_informe.py`.

## 1. Flujo General
1. **Descarga desde Chrome:** Conéctate al navegador Chrome en Windows (`25d73bab`) y descarga el archivo `.xlsx` de transacciones para el local y período requeridos.
2. **Generación del Informe:** Llama al script `generar_informe.py` utilizando el archivo `.xlsx` descargado y el propietario correspondiente:
   ```bash
   python generar_informe.py /tmp/descarga.xlsx "<Propietario>" output.pdf
   ```
3. **Presentación:** Muestra el reporte final PDF a Diego en el chat.

## 2. Documentación y Recursos de Referencia (Carga Progresiva)

Consulta los siguientes archivos según las necesidades específicas de la tarea:

- **Instrucciones detalladas de Chrome:** Consulta [`references/chrome-workflow.md`](references/chrome-workflow.md) para ver los pasos técnicos de conexión, cambio de local en el portal, control de fechas, y cómo realizar la captura y descarga del archivo `.xlsx` de forma automatizada mediante JS y Python.
- **Informes semanales automáticos:** Consulta [`references/informes-diarios.md`](references/informes-diarios.md) si Diego pide un "informe de domingo", "informe de miércoles" o "informe de jueves" para ver qué locales y en qué orden procesarlos automáticamente.
- **Mapeo de Locales y Propietarios:** Consulta la base de datos de locales en [`references/establecimientos.json`](references/establecimientos.json) para asociar correctamente cada local con su respectivo dueño.
- **Diseño del PDF y reglas del informe:** Consulta [`references/reglas-informe.md`](references/reglas-informe.md) para conocer las pautas de diseño y reglas de cálculo de comisiones e IVA del PDF de Getnet.
- **Manejo de Errores del Navegador:** Consulta [`references/manejo-errores.md`](references/manejo-errores.md) para resolver problemas de login expirado, timeouts de red, o fallas en el puerto MCP de Chrome.

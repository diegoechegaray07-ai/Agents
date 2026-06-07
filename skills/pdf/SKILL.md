---
name: pdf
description: >
  Úsala siempre que el usuario mencione un archivo .pdf o pida realizar cualquier operación
  relacionada con PDFs: leer o extraer texto/tablas, combinar/unir múltiples archivos,
  dividir un PDF en páginas, rotar páginas, rellenar formularios interactivos, desencriptar/encriptar
  archivos, extraer imágenes del documento o realizar OCR en PDFs escaneados para buscar texto.
---

# Ejecución de Skill: pdf

Esta habilidad recopila guías y mejores prácticas para procesar archivos PDF de manera eficiente mediante Python o utilidades del sistema.

## 1. Flujo de Decisión para el Agente

Determina qué tipo de operación solicita el usuario y consulta la referencia adecuada para ver ejemplos de código o comandos:

- **Extraer texto/tablas, unir, dividir o rotar páginas:** Consulta [`references/operaciones-basicas.md`](references/operaciones-basicas.md) para ejemplos con `pypdf`, `pdfplumber` y `pandas`.
- **Generar o maquetar un nuevo PDF:** Consulta [`references/creacion-pdf.md`](references/creacion-pdf.md) para guías con `ReportLab`. 
  - *¡Atención!* Lee la advertencia crítica sobre superíndices y subíndices unicode.
- **Manipular PDFs rápidamente en consola (sin scripts):** Consulta [`references/herramientas-cli.md`](references/herramientas-cli.md) para usar `pdftotext`, `qpdf` y `pdftk`.
- **Rellenar formularios PDF interactivos:** Consulta [`references/formularios.md`](references/formularios.md) para inyectar datos en AcroForms y ejecutar los scripts integrados de la skill.
- **Extraer imágenes o procesar PDFs escaneados (OCR):** Consulta [`references/ocr-scanned.md`](references/ocr-scanned.md) para guías de extracción mediante CLI y OCR con `Tesseract`.

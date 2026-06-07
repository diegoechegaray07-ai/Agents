---
name: pptx
description: >
  Úsala siempre que se involucre un archivo .pptx (de entrada, salida o ambos).
  Esto incluye: crear diapositivas, presentaciones comerciales, presentaciones de pitch;
  leer, parsear o extraer texto de archivos .pptx; editar, modificar o actualizar
  presentaciones existentes; combinar o separar archivos de diapositivas; trabajar con
  plantillas, diseños, notas del orador o comentarios. Se activa cuando el usuario
  mencione "presentación", "diapositivas", "filminas", "slides", "deck", o haga referencia
  a un archivo con extensión .pptx.
---

# Ejecución de Skill: pptx

Esta habilidad centraliza las herramientas y guías para interactuar con presentaciones de PowerPoint (`.pptx`).

## 1. Flujo de Decisión para el Agente

Dependiendo de la solicitud de Diego, ejecuta el flujo correspondiente:

- **Leer o extraer contenido de diapositivas:**
  ```bash
  # Extraer texto (genera secciones "## Slide N")
  extract-text presentacion.pptx

  # Generar una grilla de miniaturas visuales
  python scripts/thumbnail.py presentacion.pptx
  ```

- **Editar una presentación existente usando una plantilla:**
  1. Analiza el diseño de la plantilla con `python scripts/thumbnail.py`.
  2. Consulta la guía de edición en [`references/editing.md`](references/editing.md).
  
- **Crear una presentación desde cero:**
  1. Utiliza `pptxgenjs` (Javascript) cuando no haya una plantilla base.
  2. Consulta la guía y sintaxis en [`references/pptxgenjs.md`](references/pptxgenjs.md).

## 2. Pautas de Diseño y QA Visual (Obligatorio)

- **Reglas de Diseño:** Antes de generar diapositivas, lee [`references/design-guidelines.md`](references/design-guidelines.md) para inspirarte en paletas de colores, estructuras de diapositiva y tipografías, y para repasar los errores de diseño de IA que debes evitar.
- **QA Visual (Control de Calidad):** Antes de entregar la presentación, realiza obligatoriamente un proceso de verificación:
  1. Convierte las diapositivas a imágenes:
     ```bash
     python scripts/office/soffice.py --headless --convert-to pdf salida.pptx
     rm -f slide-*.jpg
     pdftoppm -jpeg -r 150 salida.pdf slide
     ls -1 "$PWD"/slide-*.jpg
     ```
  2. Invoca un subagente para realizar la inspección visual (verificando superposiciones, textos desbordados o contrastes incorrectos).

## 3. Dependencias del Entorno
- Requiere `npm install -g pptxgenjs` y `pip install Pillow`.
- La conversión a PDF requiere LibreOffice (`soffice.py`) y `pdftoppm` (Poppler).

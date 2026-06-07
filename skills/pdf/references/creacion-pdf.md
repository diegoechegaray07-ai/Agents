# Creación de PDFs con ReportLab (Python)

Este archivo contiene ejemplos de código y mejores prácticas para generar archivos PDF dinámicos utilizando la librería ReportLab.

## 1. Generación Básica de un PDF (reportlab.pdfgen.canvas)
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("documento_basico.pdf", pagesize=letter)
width, height = letter

# Agregar texto en coordenadas exactas
c.drawString(100, height - 100, "Hola Mundo")
c.drawString(100, height - 120, "Este PDF fue creado con ReportLab Canvas.")

# Agregar una línea decorativa
c.line(100, height - 130, 400, height - 130)

c.save()
```

## 2. Generación Compleja de Múltiples Páginas (reportlab.platypus)
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("reporte_flujo.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Título del reporte
title = Paragraph("Reporte de Ventas Mensuales", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

# Párrafo del cuerpo
body = Paragraph("Este es un reporte automático generado por el Agente. " * 10, styles['Normal'])
story.append(body)
story.append(PageBreak())  # Salto de página

# Página 2
story.append(Paragraph("Detalles Técnicos", styles['Heading1']))
story.append(Paragraph("Contenido detallado en la segunda página...", styles['Normal']))

# Construir el PDF
doc.build(story)
```

## 3. Advertencia Crítica de Subíndices y Superíndices Unicode

> [!WARNING]
> **NUNCA** utilices caracteres unicode directos de subíndice o superíndice (tales como `₀₁₂₃₄₅₆₇₈₉` o `⁰¹²³⁴⁵⁶⁷⁸⁹`) al generar PDFs con ReportLab.
> Los tipos de letra estándar integrados en ReportLab no disponen de estos símbolos, y se imprimirán en el PDF como cajas negras sólidas.

### Solución en Objetos Paragraph (Uso de etiquetas HTML/XML)
Utiliza las etiquetas integradas de ReportLab:
- `<sub>` para subíndices.
- `<super>` para superíndices.

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subíndice: H2O
quimica = Paragraph("Fórmula química: H<sub>2</sub>O", styles['Normal'])

# Superíndice: x² + y²
matematica = Paragraph("Ecuación: x<super>2</super> + y<super>2</super>", styles['Normal'])
```

### Solución en Dibujo Directo (Canvas)
Si dibujas con `canvas.drawString()`, debes ajustar manualmente el tamaño del texto (`setFontSize`) y la altura de la coordenada Y para emular el subíndice o superíndice.

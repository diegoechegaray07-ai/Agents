# OCR y Procesamiento de PDFs Escaneados

Este archivo detalla cómo procesar PDFs que no contienen texto digital nativo, utilizando OCR (Reconocimiento Óptico de Caracteres) y cómo extraer imágenes del documento.

## 1. Realizar OCR en un PDF Escaneado (Python)
Para PDFs que son imágenes o fotos escaneadas, primero debemos convertir las páginas a imágenes con `pdf2image` y luego aplicar OCR con `pytesseract`.

> [!NOTE]
> Requiere que la máquina tenga instalado el software de sistema **Tesseract OCR** y la librería Poppler para el renderizado de PDFs a imagen.

```python
# Requisitos: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convertir las páginas del PDF a objetos PIL Image
images = convert_from_path('escaneado.pdf')

# Procesar con OCR página por página
texto_completo = ""
for i, img in enumerate(images):
    texto_pagina = pytesseract.image_to_string(img, lang='spa') # idioma español
    texto_completo += f"--- Página {i+1} ---\n{texto_pagina}\n\n"

# Guardar texto extraído
with open("texto_ocr.txt", "w", encoding="utf-8") as f:
    f.write(texto_completo)

print("✓ Texto extraído mediante OCR exitosamente.")
```

## 2. Extraer Imágenes Embebidas (CLI)
Si el PDF contiene imágenes incrustadas dentro de sus páginas, puedes extraerlas a archivos individuales con la utilidad `pdfimages` (incluida en `poppler-utils`):

```bash
# Extraer imágenes del PDF y guardarlas con el prefijo "imagen_extraida" en formato JPEG
pdfimages -j entrada.pdf /tmp/imagen_extraida
```
Esto creará archivos como `/tmp/imagen_extraida-000.jpg`, `/tmp/imagen_extraida-001.jpg`, etc.

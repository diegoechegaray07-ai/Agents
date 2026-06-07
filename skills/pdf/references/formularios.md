# Relleno de Formularios PDF

Este archivo detalla cómo interactuar con formularios PDF interactivos (AcroForms) en Python o Javascript.

## 1. Detección de Campos Rellenables (Python - pypdf)
```python
from pypdf import PdfReader

reader = PdfReader("formulario.pdf")
fields = reader.get_fields()

# Mostrar nombre de los campos y sus valores por defecto
for field_name, field_data in fields.items():
    print(f"Campo: {field_name} | Tipo: {field_data.get('/FT')} | Valor: {field_data.get('/V')}")
```

## 2. Rellenar Campos en un Formulario PDF (Python - pypdf)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("formulario.pdf")
writer = PdfWriter()

# Clonar páginas del formulario original
writer.append(reader)

# Datos a inyectar en los campos correspondientes
data = {
    "Nombre": "Juan Pérez",
    "Fecha": "2026-06-07",
    "Monto": "15000",
}

# Rellenar los campos de la primera página
writer.update_page_form_field_values(writer.pages[0], data)

with open("formulario_completo.pdf", "wb") as output:
    writer.write(output)
```

## 3. Uso de Scripts Disponibles en la Skill
Si la skill dispone de scripts en su carpeta `scripts/`, puedes ejecutarlos para tareas específicas:

- `extract_form_structure.py` — Extrae la estructura de un formulario en formato JSON.
- `fill_fillable_fields.py` — Rellena un formulario con datos JSON.
- `check_bounding_boxes.py` — Valida la posición visual de los cuadros de texto.

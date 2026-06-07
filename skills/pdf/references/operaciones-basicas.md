# Operaciones Básicas con PDFs (Python)

Este archivo detalla cómo realizar operaciones de lectura, unión, división, rotación y extracción básica de datos de archivos PDF utilizando librerías de Python.

## 1. Lectura y Extracción Básica de Texto (pypdf)
```python
from pypdf import PdfReader

# Cargar un PDF
reader = PdfReader("documento.pdf")
print(f"Total de páginas: {len(reader.pages)}")

# Extraer el texto completo
text = ""
for page in reader.pages:
    text += page.extract_text() or ""
print(text)
```

## 2. Combinar/Unir PDFs (pypdf)
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

## 3. Dividir un PDF en Páginas Individuales (pypdf)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

## 4. Rotar Páginas (pypdf)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

# Rotar la primera página 90 grados en sentido de las agujas del reloj
page = reader.pages[0]
page.rotate(90)
writer.add_page(page)

# Copiar el resto de las páginas sin rotar
for i in range(1, len(reader.pages)):
    writer.add_page(reader.pages[i])

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

## 5. Extracción de Tablas con pdfplumber y pandas
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("documento.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Verificar que la tabla no esté vacía
                # Asumir la primera fila como cabecera
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("tablas_extraidas.xlsx", index=False)
    print("✓ Tablas guardadas en tablas_extraidas.xlsx")
```

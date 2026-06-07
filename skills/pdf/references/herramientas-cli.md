# Herramientas de Línea de Comando (CLI) para PDFs

Este archivo contiene la referencia de comandos útiles de consola para manipular archivos PDF utilizando utilidades de sistema como `pdftotext`, `qpdf`, y `pdftk`.

## 1. pdftotext (Parte de poppler-utils)
Es extremadamente rápido para extraer texto plano sin necesidad de escribir scripts de Python.

```bash
# Extraer texto de un PDF a un archivo TXT
pdftotext entrada.pdf salida.txt

# Extraer texto manteniendo la maquetación visual (muy útil para facturas/tablas)
pdftotext -layout entrada.pdf salida.txt

# Extraer solo un rango de páginas específico (páginas 1 a 5)
pdftotext -f 1 -l 5 entrada.pdf salida.txt
```

## 2. qpdf
Herramienta robusta y rápida para encriptar, desencriptar, unir, y rotar archivos PDF.

```bash
# Unir múltiples PDFs en uno solo
qpdf --empty --pages archivo1.pdf archivo2.pdf -- merged.pdf

# Extraer un rango de páginas (páginas 1 a 5) a un nuevo archivo
qpdf entrada.pdf --pages . 1-5 -- paginas1-5.pdf

# Rotar la primera página 90 grados a la derecha
qpdf entrada.pdf salida.pdf --rotate=+90:1

# Desencriptar o quitar la contraseña a un archivo PDF protegido
qpdf --password=mypassword --decrypt encriptado.pdf desencriptado.pdf
```

## 3. pdftk (si está disponible en el sistema)
Una alternativa clásica para manipulación de PDFs.

```bash
# Unir archivos
pdftk archivo1.pdf archivo2.pdf cat output unido.pdf

# Dividir todas las páginas del documento (genera pg_0001.pdf, pg_0002.pdf, etc.)
pdftk entrada.pdf burst

# Rotar la primera página hacia el este (90 grados horario)
pdftk entrada.pdf rotate 1east output rotado.pdf
```

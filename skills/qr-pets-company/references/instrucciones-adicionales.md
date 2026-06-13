# Instrucciones Adicionales y Notas de Desarrollo (QR Pets Company)

Este archivo contiene información complementaria sobre la validación de materiales de cobro generados y consideraciones técnicas de desarrollo.

---

## 1. Validación y Control de Calidad (Post-Regeneración)
Una vez que el orquestador finalice, realiza obligatoriamente los siguientes pasos de control visual:
1. Lee los archivos de vista previa generados:
   - `cartel_petscompany.png`
   - `sticker_petscompany.png`
2. Muestra a Diego una vista previa de los resultados (al menos el sticker y el cartel A4) en el chat para que confirme su diseño.
3. Si Diego solicita ajustes visuales (cambios en el tamaño de letra, colores, logos o espaciado), ten en cuenta que estos parámetros están definidos y deben editarse dentro del código fuente del proyecto:
   - Orquestador y Sticker: `src/sticker_petscompany.py`
   - Cartel A4: `src/cartel_a4_pdf.py`
   - Cartel Base: `src/qr_petscompany.py`
   - Kit de Marca Central: `src/design_kit.py`

---

## 2. Consideraciones Técnicas y de Desarrollo
- **Idioma del Agente:** Mantén las confirmaciones y comunicaciones en español. Pide confirmación al usuario antes de borrar archivos locales o realizar operaciones destructivas.
- **Manejo de Git:** El repositorio de control de versiones está en la carpeta raíz `Antigravity/` (un nivel arriba del proyecto QR). Al hacer commits, stagea únicamente archivos explícitos del subdirectorio `QR/` (evita `git add .`, para no incluir archivos temporales de OneDrive).
- **Dependencias:** El entorno de Python de Diego ya tiene preinstaladas las librerías `qrcode` y `Pillow`. No intentes instalar dependencias a menos que falten explícitamente en la ejecución.

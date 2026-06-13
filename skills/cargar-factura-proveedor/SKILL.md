---
name: cargar-factura-proveedor
description: >
  Lee facturas de proveedores —en PDF o en foto/imagen (JPG, JPEG, PNG)—,
  extrae los datos clave con OCR y las registra como factura de compra (Bill) en
  la API de Alegra. Úsala cuando el usuario suba un PDF o una foto de una factura,
  arrastre la imagen de un ticket, o diga frases como "leé esta factura y cargala
  en alegra", "cargá la foto de esta factura", "registrá esta compra del proveedor X",
  "subí este ticket de gasto a Alegra".
---

# Habilidad: Cargar Factura de Proveedor en Alegra (PDF o foto)

Procesa facturas de proveedores —en PDF o imagen— y las registra en Alegra.
Funciona igual para ambos formatos: la única diferencia es el archivo de entrada.

### Pasos Clave:

1. **Lectura con OCR del archivo:**
   - Utiliza `view_file` en la ruta absoluta del archivo (PDF, JPG, JPEG o PNG).
   - Extrae CUIT, Razón Social, Fecha, Número de Comprobante, Importe Total e ítems individuales.

2. **Búsqueda e Identificación de Artículos / Sugerencia de Categoría:**
   - Si la factura contiene artículos detallados (ej. alimento balanceado), busca los artículos en el catálogo de Alegra para obtener sus IDs. Si no existen, sugiérele al usuario crearlos como productos inventariables.
   - Si la factura es de gasto general (servicios, fletes), compárala contra las cuentas de Pets Company frecuentes (ej. `5148` para Costos del inventario, `5193` para fletes, `5214` para gastos generales).

3. **Confirmación con el Usuario:**
   - Muestra los datos extraídos (y desglose de artículos si corresponde) en una tabla y pide confirmación antes de la subida.

4. **Registro en Alegra:**
   - Script: `Alegra Pets Company/tools/upload_provider_bill.py`
   - Si tiene artículos desglosados, usa `--items-json`.
   - Si es gasto general, usa `--category-id` y `--amount`.

### Reglas Especiales de Creación y Carga:
- **Creación de Artículos:** costo neto de descuento; precio venta = `costo_neto × 1.6`, centena arriba.
- **Actualización de Costos:** solo si el nuevo costo neto es mayor al existente.
- **Conflictos de Referencia:** prefijo del proveedor si la referencia está duplicada.
- **Marcas 'NO':** omitir esos ítems del JSON.

5. **Notificar Resultado:** ID Alegra, número, total, estado.

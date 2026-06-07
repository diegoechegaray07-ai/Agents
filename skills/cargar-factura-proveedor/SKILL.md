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
   - Si tiene artículos desglosados, genera el JSON para el parámetro `--items-json` y ejecuta:
     ```bash
     python3 upload_provider_bill.py \
       --provider-name "[Proveedor]" \
       --provider-id "[CUIT]" \
       --date "[Fecha YYYY-MM-DD]" \
       --number "[N° Comprobante]" \
       --status "open" \
       --items-json '[{"id": "...", "price": ..., "quantity": ..., "discount": ...}]'
     ```
   - Si es gasto general, ejecuta:
     ```bash
     python3 upload_provider_bill.py \
       --provider-name "[Proveedor]" \
       --provider-id "[CUIT]" \
       --date "[Fecha YYYY-MM-DD]" \
       --number "[N° Comprobante]" \
       --amount [Monto] \
       --category-id "[ID Categoría]" \
       --description "[Concepto]" \
       --status "open"
     ```
     *(Nota: En entornos locales, si `tools/upload_provider_bill.py` arroja un error de permiso debido a sandboxing de macOS/OneDrive, ejecuta la copia ubicada directamente en la raíz: `python3 upload_provider_bill.py`)*

### Reglas Especiales de Creación y Carga:
- **Margen de Ganancia, Redondeo y Actualización de Costos:**
  - **Creación de Artículos:** Si un artículo no existe en el catálogo, se crea aplicando el margen de ganancia correspondiente sobre el costo unitario de la factura (ej. `precio_venta = costo * 1.5` para un 50% de recargo, o `costo * 1.4` para un 40%). El precio de venta final debe ser **redondeado siempre para arriba a la centena de pesos más cercana** (ej. de $1204.88 a $1300, de $17690.61 a $17700, de $7157.89 a $7200).
  - **Actualización de Costos:** Si el artículo ya existe, **solo se actualiza su costo (y se recalcula su precio de venta con el margen y redondeo correspondientes) en Alegra si el nuevo costo de la factura es estrictamente mayor al costo existente**. Si el nuevo costo es menor o igual al existente, se mantiene sin cambios en el catálogo.
- **Conflictos de Referencia:** Si el código de referencia ya está en uso por otro producto de Alegra, se debe anteponer el prefijo del proveedor (ej. `MP-` para Maipu, `MP-344`) para evitar errores de duplicidad.
- **Notas y marcas manuales (ej. 'NO'):** Si algún ítem en la factura tiene una marca manual como "NO" o similar indicando que no debe ser incluido, este artículo se debe omitir por completo del JSON y restar del total del comprobante.

5. **Notificar Resultado:**
   - Reporta el ID de Alegra, N° definitivo, total y estado devuelto.

---
name: getnet-informe
description: >
  Genera informes PDF de ventas a partir de archivos Excel (.xlsx) descargados
  del portal Getnet (globalgetnet.com). Úsalo siempre que el usuario suba uno o
  más archivos xlsx de Getnet y pida un informe, reporte, resumen o análisis de
  ventas. También aplica cuando el usuario dice "realizame el informe", "generá
  el informe de ventas", "informe como siempre" o frases similares después de
  descargar transacciones. No esperar que el usuario describa el formato: este
  skill define exactamente cómo debe verse el informe.
---

# Skill: Informe de Ventas Getnet

Genera informes PDF profesionales de ventas a partir de archivos `.xlsx`
exportados desde el portal Getnet.

---

## Reglas de negocio

### Mapeo de establecimientos
El mapeo establecimiento → propietario es **dato canónico** en
[references/establecimientos.json](references/establecimientos.json); el script lo
lee de ahí (`resolver_propietario`). No lo repitas acá para que no se desincronice.

- El nombre del establecimiento **nunca** aparece en el informe; solo el propietario
- Si el establecimiento no está en el JSON, usar el nombre tal como viene

### Columnas del detalle de transacciones
**Mostrar:** Fecha de Operación, Billetera, Marca, Tipo, Nro de Cupón, Monto Bruto  
**Omitir siempre:** Arancel, IVA Arancel, Costo Pago Inmediato, IVA Pago Inmediato  
**Plan Cuotas:** incluir la columna solo si al menos una fila tiene valor (no vacío / NaN / 0)  
**Monto Neto:** mostrar solo si `Costo Financiero` o `IVA CFT` tienen valores > 0  
**Monto Bruto:** nunca restar aranceles ni IVA; usar el valor del campo `Monto Bruto Transacción` tal cual

### KPIs (portada)
Monto Bruto · Transacciones · Ticket Promedio · Ticket Máximo · Ticket Mínimo  
Agregar **Monto Neto** solo si aplica (ver regla anterior)  
**No incluir:** Liquidadas / Pendientes

### Tablas de resumen
- Ventas por Día + Ventas por Marca → **lado a lado** en la misma fila
- Ventas por Tipo de Tarjeta → a ancho completo debajo
- Cada tabla con fila de total al pie
- Si aplica Monto Neto: agregarlo como columna extra en todas las tablas

### Estructura del PDF
- **Página 1:** Encabezado + KPIs + 3 tablas de resumen (todo sin cortes)
- **Página 2+:** Detalle de transacciones (salto de página explícito)
- El encabezado **solo aparece en la página 1**

---

## Diseño visual

El diseño (paleta azul, encabezado, KPIs, tablas) ya está implementado en
`scripts/generar_informe.py`. Si vas a **modificar** el diseño, leé
[references/diseno.md](references/diseno.md); para generar el informe no hace falta.

---

## Cómo ejecutar

### Paso 1 — Leer el archivo

```python
import pandas as pd
df = pd.read_excel('/mnt/user-data/uploads/<archivo>.xlsx')
```

### Paso 2 — Determinar propietario

El script resuelve automáticamente el propietario según el mapeo. Pasá el nombre del establecimiento (ej. `"DCG 8"`) y el script lo convierte al propietario correspondiente.

### Paso 3 — Ejecutar el script

```bash
python /path/to/skill/scripts/generar_informe.py \
  /mnt/user-data/uploads/<archivo>.xlsx \
  "<propietario>" \
  /mnt/user-data/outputs/<Informe_Propietario>.pdf
```

El script está en `scripts/generar_informe.py` dentro de este skill.  
Acepta 3 argumentos: ruta xlsx · nombre propietario · ruta pdf de salida.

### Paso 4 — Presentar

```python
# Llamar a present_files con la ruta del PDF generado
```

---

## Dependencias

```
pandas
openpyxl      # para leer .xlsx
reportlab     # para generar PDF
```

Instalar si no están disponibles:
```bash
pip install pandas openpyxl reportlab --break-system-packages -q
```

---

## Notas importantes

- El script maneja automáticamente la columna **Plan Cuotas** (la omite si está vacía)
- El script maneja automáticamente **Monto Neto** (lo omite si no hay CFT/IVA CFT)
- Los anchos de columna del detalle están calibrados al contenido real de Getnet
- Si se procesan **múltiples archivos**, ejecutar el script una vez por cada xlsx y presentar todos los PDFs juntos al finalizar

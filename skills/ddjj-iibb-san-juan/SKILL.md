---
name: ddjj-iibb-san-juan
description: >
  Genera la liquidación de la DDJJ mensual de Ingresos Brutos de San Juan
  (régimen LOCAL) a partir de un archivo Excel (.xlsx) de "Mis Comprobantes
  Emitidos" de ARCA (ex-AFIP). Calcula la base imponible (neto gravado del
  período, neteando notas de crédito), aplica la alícuota (3% general por
  defecto, parametrizable), resta las deducciones que indique el usuario
  (retenciones, percepciones, percepciones bancarias, saldo a favor anterior)
  y produce un PDF de liquidación con el saldo a pagar, listo para cargar en
  la presentación web de la DGR San Juan (rentas.dgrsj.gob.ar) o en el
  aplicativo SIAP. Úsalo SIEMPRE que Diego suba un xlsx de ARCA y diga cosas
  como "hacé la DDJJ de ingresos brutos", "liquidá IIBB San Juan",
  "calculá ingresos brutos del mes", "DDJJ de rentas San Juan", o cualquier
  variante de declaración jurada / liquidación de ingresos brutos de San Juan.
---

# Skill: DDJJ Ingresos Brutos — San Juan (régimen local)

Genera la **liquidación mensual del Impuesto sobre los Ingresos Brutos** de la
provincia de San Juan (contribuyente **local**) a partir del Excel de
"Mis Comprobantes Emitidos" de ARCA, y produce un PDF de liquidación con el
saldo a pagar — los mismos números que después se cargan **manualmente** en la
presentación web de la DGR ([rentas.dgrsj.gob.ar](https://rentas.dgrsj.gob.ar))
o en el aplicativo SIAP.

---

## Cómo funciona la presentación (contexto)

La DGR San Juan **no importa archivos en la web**: la carga es manual. Por eso
el entregable clave de esta skill es un **PDF de liquidación** con los importes
exactos a tipear: período, base imponible, alícuota, impuesto determinado,
deducciones y saldo a pagar. Ese mismo cálculo sirve si la presentación se hace
por el aplicativo SIAP.

> Si en el futuro Diego provee un archivo de importación de ejemplo del
> aplicativo SIAP, agregar un generador de ese archivo en `scripts/` y
> documentarlo acá. Por ahora la skill produce solo el PDF de liquidación.

---

## Entrada esperada

Archivo Excel de ARCA con header en **fila 2** (leer con `header=1`). Columnas
clave (mismas que usa la skill `arca-informe`):

| Columna | Uso |
|---|---|
| `Fecha` | Fecha de emisión (`dd/mm/yyyy`) — determina el período |
| `Tipo` | Tipo de comprobante (ej. `1 - Factura A`, `3 - Nota de Crédito A`) |
| `Denominación Receptor` | Cliente (informativo) |
| `Neto Gravado Total` | **Base imponible** de IIBB (sin IVA) |
| `Neto No Gravado` | Informativo (no integra base gravada) |
| `Imp. Total` | Total del comprobante (informativo) |

---

## Datos que pide al usuario al correr la skill

Antes de generar, confirmar con Diego (preguntar solo lo que falte):

1. **Período** a liquidar (mes/año). Por defecto, inferirlo de las fechas del
   xls (el mes predominante).
2. **Contribuyente y CUIT** (para el encabezado). Si no se sabe, dejar el
   encabezado genérico y avisarle.
3. **Alícuota**: por defecto **3%** (alícuota general de comercio/servicios,
   Ley Impositiva 2730-I San Juan). Confirmar si esta actividad usa otra.
4. **Deducciones** (todas opcionales, default 0): retenciones, percepciones,
   percepciones bancarias/aduaneras, **saldo a favor del período anterior**.

No inventar deducciones: si Diego no las menciona, van en 0.

---

## Reglas de cálculo (régimen local)

- **Base imponible** = suma de `Neto Gravado Total` del período, **neteando
  las notas de crédito** (los comprobantes cuyo `Tipo` contiene "crédito" /
  "credito" restan). Las notas de débito suman.
- **Impuesto determinado** = `base_imponible × alícuota`.
- **Total deducciones** = retenciones + percepciones + percepciones bancarias +
  saldo a favor anterior.
- **Saldo**:
  - Si `impuesto_determinado − total_deducciones > 0` → **saldo a pagar**.
  - Si es `< 0` → **saldo a favor** para el período siguiente (no se paga).
- Montos formateados `$ 1.234,56` (punto de miles, coma decimal).

---

## Generar el PDF

Usar el script bundleado, que hace el cálculo y arma el PDF:

```bash
python "scripts/generar_ddjj_sanjuan.py" \
  --xlsx "<ruta al xlsx de ARCA>" \
  --salida "<ruta de salida .pdf>" \
  --periodo "MM/AAAA" \
  --contribuyente "Razón Social" \
  --cuit "30-12345678-9" \
  --alicuota 3.0 \
  --retenciones 0 \
  --percepciones 0 \
  --perc-bancarias 0 \
  --saldo-favor-anterior 0
```

- Solo `--xlsx` y `--salida` son obligatorios; el resto tiene defaults
  (alícuota 3%, deducciones 0, período inferido de las fechas).
- El script imprime por consola el resumen del cálculo (base, impuesto,
  deducciones, saldo) además de generar el PDF — revisar ese resumen y
  reportárselo a Diego junto con la ruta del PDF.
- Si falta alguna librería (`pandas`, `openpyxl`, `reportlab`), instalarla.

Si el script falla por una variante de formato del xls (nombres de columna
distintos), leer el archivo, identificar las columnas equivalentes y ajustar,
o pasar la base imponible ya calculada con `--base-imponible <monto>` (override
que saltea la lectura del Neto Gravado).

---

## Diseño del PDF

El diseño (acento verde `#059669`, encabezado, KPIs, tablas) ya está
implementado en `scripts/generar_ddjj_sanjuan.py`. Si vas a **modificar** el
diseño, leé [references/diseno.md](references/diseno.md); para liquidar
normalmente no hace falta.

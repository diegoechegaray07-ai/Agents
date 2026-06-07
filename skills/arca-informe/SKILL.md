---
name: arca-informe
description: >
  Genera informes PDF profesionales a partir de archivos Excel (.xlsx) de
  "Mis Comprobantes Emitidos" descargados del portal ARCA (ex-AFIP), con CUIT
  33-71660647-9. Úsalo siempre que Diego suba un archivo xlsx de ARCA/AFIP y
  pida un informe, reporte o resumen. También aplica cuando diga "haceme el
  informe de ARCA", "informe de comprobantes", "reporte de facturas", o
  cualquier variante similar. No esperar que describa el formato: este skill
  define exactamente cómo debe verse el informe.
---

# Skill: Informe de Comprobantes Emitidos — ARCA

Genera informes PDF profesionales a partir de archivos `.xlsx` exportados
desde el portal ARCA (ex-AFIP), sección "Mis Comprobantes Emitidos".

---

## Entrada esperada

Archivo Excel con header en fila 2 (leer con `header=1`). Columnas clave:

| Columna | Uso |
|---|---|
| `Fecha` | Fecha de emisión (string `dd/mm/yyyy`) |
| `Tipo` | Tipo de comprobante (ej. `1 - Factura A`) |
| `Número Desde` | Número del comprobante |
| `Denominación Receptor` | Nombre del cliente (aplicar `.title()`) |
| `Neto Gravado Total` | Base imponible |
| `Neto No Gravado` | Monto no gravado |
| `IVA 21%` | IVA al 21% (puede haber otras alícuotas; incluir solo las que tengan valores > 0) |
| `Total IVA` | Total IVA sumado |
| `Imp. Total` | Total del comprobante |

---

## Cómo ejecutar

Ejecuta el script de generación de reporte en Python con el archivo Excel de entrada:

```bash
python3 tools/generate_arca_report.py "[ruta_al_excel]" -o "[ruta_de_salida_pdf]"
```

Ejemplo de uso:
```bash
python3 tools/generate_arca_report.py "Facturación/Mayo/DCG/Mis Comprobantes Emitidos - CUIT 33716606479.xlsx" -o "Arca/Informe_ARCA.pdf"
```

---

## Diseño visual

El diseño (paleta, encabezado, KPIs, tablas) ya está implementado en
`tools/generate_arca_report.py`. Si vas a **modificar** el diseño, leé
[references/diseno.md](references/diseno.md); para generar el informe normal no
hace falta.

---

## Estructura del PDF

### Página 1

**Encabezado** (dibujado en canvas, no como flowable)

**KPIs** — 4 tarjetas horizontales

**Resumen por Receptor** *(KeepTogether: título + tabla)*
Columnas: Receptor | N° | Neto Gravado | IVA 21% | Total
Ordenado por Total descendente. Fila de total al pie.

**Ventas por Fecha** *(KeepTogether: título + tabla)*
Columnas: Fecha | N° | Neto Gravado | IVA 21% | Total
Fila de total al pie.

### Página 2+ (salto explícito)

**Detalle de Comprobantes Emitidos** *(título + tabla con repeatRows=1)*
Columnas: Fecha | N° Comp. | Receptor | Neto Grav. | IVA 21% | Total | % IVA
- `% IVA` = `IVA / Neto * 100`, formateado como `"21%"`
- Fila de total al pie (% IVA muestra alícuota principal)

---

## Reglas de negocio

- IVA: mostrar **solo las alícuotas que tengan suma > 0** en los datos. Si solo hay IVA 21%, mostrar solo esa columna.
- Montos formateados como `$ 1.234,56` (punto miles, coma decimal).
- Nombres de receptores siempre en `.title()` (capitalizar cada palabra).
- Si `Neto No Gravado` es 0 para todos, igualmente mostrar el KPI (con valor `$ 0,00`).
- El encabezado completo aparece **solo en la página 1**; páginas siguientes usan el mini-header.

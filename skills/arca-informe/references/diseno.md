# Diseño visual — Informe ARCA

> Esto ya está implementado en `tools/generate_arca_report.py`. Leé este archivo
> solo si vas a **modificar** el diseño del PDF; para generar el informe normal
> no hace falta.

## Paleta
- `C_BANDA`      = `#3B82F6`  (celeste vivo — banda lateral y acentos)
- `C_HEADER_BG`  = `#0F172A`  (azul muy oscuro — fondo encabezado)
- `C_HEADER_MID` = `#1E3A5F`  (azul medio — panel derecho del encabezado)
- `C_ACENTO`     = `#60A5FA`  (celeste claro — valores KPI secundarios)
- `C_ACENTO2`    = `#93C5FD`  (celeste muy claro — labels, subtítulos)
- `C_TABLE_HDR`  = `#1E3A5F`  (fondo encabezado de tablas)
- `C_ALT`        = `#EFF6FF`  (filas alternas)
- `C_TOT_BG`     = `#DBEAFE`  (fila de totales)
- `C_TOT_LINE`   = `#3B82F6`  (línea superior fila total)
- `C_BOX`        = `#BFDBFE`  (borde exterior tablas)
- `C_GRID`       = `#DBEAFE`  (grilla interna)
- `C_SEC_BG`     = `#F0F7FF`  (fondo títulos de sección)
- `C_MUTED`      = `#64748B`  (texto pie de página)

## Encabezado (altura: 48mm)
- Fondo dividido: mitad izquierda `C_HEADER_BG`, mitad derecha `C_HEADER_MID`
- Banda lateral izquierda de 5mm en `C_BANDA`
- Línea inferior de 1.5mm en `C_BANDA`
- **Ícono rombo** (CE) a la izquierda en `C_BANDA`, iniciales en blanco
- **Título** "Comprobantes Emitidos" en blanco, 18pt bold
- **Subtítulo** CUIT en `C_ACENTO2`, 9pt
- Separador horizontal interno a los 25mm desde arriba
- **3 chips** en fila horizontal (fondo `#0A1628`, acento top `C_BANDA`):
  - PERÍODO: `{fecha_min} → {fecha_max}`
  - COMPROBANTE: tipo único (ej. "Factura A") o "Varios" si hay más de uno
  - CANTIDAD: `{n} facturas`
- Footer en todas las páginas: línea `C_BOX` + fecha de generación (izq.) + número de página (der.)

## Mini-header (páginas 2+, altura: 12mm)
- Fondo `C_HEADER_BG`, banda lateral 4mm `C_BANDA`, línea inferior 1mm `C_BANDA`
- Título + CUIT en blanco (izq.) · Período en `C_ACENTO2` (der.)

## KPIs (justo después del encabezado)
4 tarjetas en una fila, fondo `C_HEADER_BG`, línea superior 3pt `C_BANDA`:
1. **TOTAL FACTURADO** — `Imp. Total` total, valor en blanco 15pt bold
2. **NETO GRAVADO** — `Neto Gravado Total`, valor en `C_ACENTO` 11pt bold
3. **IVA 21%** — suma de `IVA 21%` (o la alícuota presente), valor en `C_ACENTO` 11pt bold
4. **NETO NO GRAVADO** — `Neto No Gravado`, valor en `C_ACENTO` 9pt bold

## Títulos de sección
Caja con fondo `C_SEC_BG`, banda izquierda 4pt `C_BANDA`, borde 0.5pt `C_BOX`.
Texto 9.5pt bold `C_TABLE_HDR`, padding izquierdo 9pt.
**Usar `KeepTogether`** para que el título nunca se separe de su tabla.

## Tablas (todas)
- Encabezado: fondo `C_TABLE_HDR`, texto blanco 7.5pt bold, línea inferior 2pt `C_BANDA`
- Filas alternas: blanco / `C_ALT`
- Fila total: fondo `C_TOT_BG`, texto bold `C_TABLE_HDR`, línea superior 1.5pt `C_TOT_LINE`
- Borde exterior: 0.8pt `C_BOX`
- Grilla interna: 0.3pt `C_GRID`
- Padding celdas: 4pt top/bottom, 5pt left/right
- Tamaño texto: 7.5pt, leading = size × 1.25
- **Los anchos de columna deben ajustarse al contenido** para que no se corte ningún valor

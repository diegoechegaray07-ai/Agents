# Reglas del Informe PDF — Getnet

## Reglas de negocio

### Mapeo de establecimientos → propietario
- **DCG 1 / DCG1** → `Ayrton Gil`
- **DCG 2 / DCG2** → `Jacqueline Muñoz`
- **DCG 4 / DCG4** → `Martin Costa`
- **DCG 5 / DCG5** → `Lucas Balmaceda`
- **DCG 7 / DCG7** → `Jose Castro`
- **DCG 8 / DCG8** → `Sebastián Mas`
- **DCG 9 / DCG9** → `Pets Company`
- Resto → usar el nombre del establecimiento tal cual

### Filtrado de transacciones rechazadas
- **Regla:** Cualquier transacción cuyo estado comience con la palabra "rechaza" (ej. "Rechazada", "Rechazado", "Rechazadas", etc., caso insensible a mayúsculas/minúsculas) debe ser **completamente desestimada** de todos los cálculos del reporte, KPIs, tablas de resumen y detalle.
- **Detección:** Buscar la columna con nombre "Estado" (o cualquier columna que contenga la palabra "estado" de manera insensible).

### Columnas del detalle de transacciones
| Columna | Regla |
|---------|-------|
| Fecha de Operación | Siempre mostrar |
| Billetera | Siempre mostrar |
| Marca | Siempre mostrar |
| Tipo | Siempre mostrar |
| Nro de Cupón | Siempre mostrar |
| Plan Cuotas | **Solo si** al menos 1 fila tiene valor (no vacío/NaN/0) |
| Monto Bruto | Siempre mostrar — usar campo `Monto Bruto Transacción` sin descuentos |
| Monto Neto | **Solo si** `Costo Financiero` o `IVA CFT` > 0 |

**Omitir siempre:** Arancel, IVA Arancel, Costo Pago Inmediato, IVA Pago Inmediato  
**No restar** ningún cargo al Monto Bruto

### KPIs (página 1)
- Monto Bruto · Transacciones · Ticket Promedio · Ticket Máximo · Ticket Mínimo
- Agregar **Monto Neto** solo si aplica la regla anterior
- **No incluir:** Liquidadas / Pendientes

### Tablas de resumen (página 1)
- **Ventas por Día** + **Ventas por Marca** → lado a lado
- **Ventas por Tipo de Tarjeta** → ancho completo, debajo
- Cada tabla: fila de total al pie con suma
- Si aplica Monto Neto: columna extra en todas las tablas

---

## Estructura del PDF

### Página 1 — Resumen
1. Encabezado (solo aquí)
2. KPIs
3. Tabla Ventas por Día | Tabla Ventas por Marca (lado a lado)
4. Tabla Ventas por Tipo de Tarjeta (ancho completo)

### Página 2+ — Detalle
- `PageBreak()` explícito antes del detalle
- Sin encabezado en páginas siguientes
- Tabla completa de transacciones con columnas según reglas arriba

---

## Diseño visual

### Paleta de colores
```
AZUL_OSC    = #0D3B6E   # portada / encabezado fondo
AZUL_MED    = #1B4F8A   # headers de tablas, KPI label
AZUL_ACENTO = #4DA3E0   # banda lateral, líneas de acento
AZUL_KPI_BG = #EBF4FF   # fondo tarjetas KPI
AZUL_SEC_BG = #F0F7FF   # fondo títulos de sección
AZUL_ROW1   = #EBF4FF   # filas alternas
AZUL_TOTAL  = #D0E8FB   # fila total
```

### Encabezado
- Banda lateral izquierda celeste (`0.55cm`) + bloque de texto fondo azul oscuro
- Jerarquía de texto:
  - `INFORME  DE  VENTAS` — pequeño, espaciado, color `#80B8DC`
  - Nombre del propietario — grande (20pt), blanco, negrita
  - `Período  DD/MM/YYYY — DD/MM/YYYY` — gris claro

### KPIs
- Cada tarjeta: header azul oscuro con label en blanco + cuerpo con valor + línea inferior celeste
- Distribuidas en filas de hasta 5

### Títulos de sección
- Barra lateral celeste (`0.22cm`) + texto sobre fondo suave (`#F0F7FF`)

### Tablas
- Header: fondo `#1B4F8A`, texto blanco, línea inferior celeste
- Filas: alternadas blanco / `#EBF4FF`
- Total: fondo `#D0E8FB`, negrita, línea superior azul
- Grid: `#AACCEE` (0.25pt)

---

## Anchos de columna — Detalle de transacciones
Calibrados al contenido real de Getnet (fuente 7.2pt):

| Columna | Ancho fijo |
|---------|----------|
| Fecha de Operación | 2.85 cm |
| Billetera | 2.50 cm |
| Marca | 1.60 cm |
| Tipo | 2.40 cm |
| Nro de Cupón | 2.85 cm |
| Plan Cuotas | 1.40 cm (si aplica) |
| Monto Bruto | resto del ancho disponible |

---

## Dependencias Python
```
pandas
openpyxl
reportlab
```

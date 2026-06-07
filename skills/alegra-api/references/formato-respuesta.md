# Formato de Respuesta de Reporte de Ventas (Alegra)

Siempre que presentes un análisis de ventas, facturas o movimientos a Diego, debes estructurar la respuesta de la siguiente manera:

## 1. Resumen Ejecutivo
Destaca las métricas clave del período analizado:
- **Total Facturado:** Expresado en pesos argentinos con formato `$ 1.234,50` (usa `format_ars`).
- **Cantidad de Ventas:** Número total de facturas.
- **Ticket Promedio:** Total facturado / cantidad de ventas.

## 2. Tablas de Análisis
Usa las siguientes estructuras de tabla markdown según corresponda:

### Tabla de Facturas Individuales
| Hora | Total | Pago | Productos |
|---|---|---|---|
| 10:15 | $ 12.500,00 | Efectivo | Alimento Balanceado 15kg, Pipeta |

### Tabla de Resumen por Categoría o Turno
| Categoría | Facturas | Total | Prom/venta |
|---|---|---|---|
| Mañana | 15 | $ 150.000,00 | $ 10.000,00 |
| Noche | 10 | $ 120.000,00 | $ 12.000,00 |

## 3. Mapeo de Medios de Pago
Mapea los códigos internos de la API a nombres legibles para Diego:
- `cash` ➔ **Efectivo**
- `debit-card` ➔ **Débito**
- `transfer` ➔ **Transferencia**
- `credit-card` ➔ **Crédito**
- Cualquier otro código debe mostrarse tal cual.

## 4. Observaciones
Incluye un breve análisis cualitativo:
- La venta más grande del día/período.
- Patrones de horarios detectados (mañana vs noche).
- Anomalías detectadas.

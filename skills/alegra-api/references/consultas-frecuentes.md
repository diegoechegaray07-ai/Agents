# Consultas Frecuentes y Cómo Resolverlas

Este archivo contiene la lógica analítica para responder las peticiones habituales de Diego.

## 1. "Ventas de hoy / ayer / esta semana / este mes"
- Determina la fecha del sistema o del período solicitado.
- Llama a `cli.invoices_on(fecha)` o `cli.invoices_between(inicio, fin)`.
- Genera el reporte con el formato definido en `references/formato-respuesta.md`.

## 2. "Cómo fue la mañana o la tarde"
- Obtén las facturas del día analizado.
- Clasifica cada factura en turnos usando la función `turno()` del cliente compartido:
  - **Mañana:** hora < 14:00 (facturas registradas entre las 09:30 y 13:59).
  - **Noche:** hora >= 17:30 (facturas registradas a partir de las 14:00).
- Sumariza totales por turno y presenta la comparación.

## 3. "Detalle de la factura X"
- Busca en la lista de facturas de la sesión por `numberTemplate.formattedNumber` (ejemplo: `00001252`).
- Si no está cargada en los archivos JSON temporales de la sesión, descarga páginas adicionales.
- Muestra el emisor, receptor, lista de ítems, precio, subtotal, impuestos y medio de pago.

## 4. "Ventas del producto o referencia X"
- Obtén las facturas del período.
- Itera sobre los `items` de cada factura.
- Filtra las coincidencias donde `item.get('reference') == 'X'` o `item.get('name')` contenga la cadena de búsqueda.
- Consolida cantidad vendida, total recaudado y facturas asociadas.

## 5. "Análisis por medio de pago"
- Obtén las facturas.
- Agrupa por el medio de pago (primer elemento de la lista `payments` de la factura).
- Mapea el código usando `map_payment_method` y calcula cantidad de operaciones, total de pesos facturados y porcentaje sobre el total del día.

## 6. "Análisis por horario / ¿cuándo conviene abrir?"
- Agrupa las facturas del período por hora entera (ej: `10`, `11`, `18`).
- Calcula el total facturado y la cantidad de transacciones para cada hora.
- Analiza la distribución entre turnos de mañana y noche para recomendar las horas más concurridas.

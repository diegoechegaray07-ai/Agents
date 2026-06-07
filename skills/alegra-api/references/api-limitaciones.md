# Limitaciones de la API de Alegra

Consulte este archivo si tiene problemas al realizar llamadas de API o si obtiene resultados incorrectos en los filtros.

## Limitaciones Conocidas
1. **Límite de registros por solicitud (Paginación):**
   La API de Alegra permite un tope máximo de **30 facturas/elementos** por llamada. Si necesitas un período más amplio o gran volumen de datos, debes paginar utilizando los parámetros `limit` y `start` (ej: `start=0`, `start=30`, `start=60`).

2. **Filtro de fecha del servidor inestable:**
   Los parámetros de filtrado server-side de fechas (`date_start` y `date_end`) no funcionan de forma consistente ni fiable.
   - **Workaround:** Descarga siempre múltiples páginas para abarcar de sobra el período necesario y filtra los datos por fecha localmente (en Python o JS).

3. **Orden por defecto:**
   Las facturas son devueltas por defecto ordenadas de la más reciente a la más antigua.

4. **Búsqueda por número de factura:**
   Para buscar una factura por su número con formato legible (ej: `00001252`), debes inspeccionar el campo `numberTemplate.formattedNumber` dentro de cada factura obtenida.

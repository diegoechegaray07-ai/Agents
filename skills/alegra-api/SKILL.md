---
name: alegra-api
description: >
  Consulta y analiza ventas, facturas, productos y medios de pago desde la API de Alegra
  para Pets Company (veterinaria/petshop, San Juan, Argentina). Úsala siempre que el usuario
  pregunte por ventas del día, semana o mes; cómo fue la mañana o la tarde; qué se vendió;
  cuánto se facturó; análisis por medio de pago; detalle de una factura; búsqueda por producto
  o referencia; o cualquier consulta sobre datos comerciales. También aplica cuando el usuario
  diga "cómo fueron las ventas", "qué vendimos", "cuánto hicimos hoy/ayer/esta semana",
  "detalle de la factura X", "buscá el producto Y", o frases similares relacionadas con
  movimientos comerciales del negocio.
---

## Contexto del negocio

- **Empresa:** Pets Company — Echegaray, Diego Andres (CUIT 20-33059551-6)
- **Rubro:** Veterinaria / petshop, San Juan, Argentina
- **Moneda:** ARS (pesos argentinos)
- **Horario:** Lunes a Sábado · Mañana 9:30–14:00 · Noche 17:30–21:00 · Domingo cerrado

## Credenciales API

- **Base URL:** `https://app.alegra.com/api/v1/`
- **Auth:** HTTP Basic. Las credenciales **no van en este archivo** (para no
  filtrarlas si la skill se versiona): viven en el `.env` de esta carpeta
  (gitignored), en `ALEGRA_USER` y `ALEGRA_TOKEN`.

Cargá el `.env` de la skill antes de llamar a la API, y usá las variables:

```bash
set -a; source .env; set +a   # desde la carpeta de la skill alegra-api
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "https://app.alegra.com/api/v1/invoices?limit=30&start=0"
```

## Limitaciones importantes de la API

- El límite máximo por request es **30 facturas**. Para períodos más largos, paginar con `start=0`, `start=30`, `start=60`, etc.
- El filtro `date_start` / `date_end` **no funciona de forma confiable** — siempre traé múltiples páginas y filtrá por fecha en Python.
- Las facturas vienen ordenadas de más reciente a más antigua por defecto.
- Para buscar una factura por número formateado (ej. `00001252`), buscá en los datos cacheados por `numberTemplate.formattedNumber`.

## Cómo paginar y filtrar

```bash
# Traer páginas hasta cubrir el período necesario (con .env ya cargado)
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "URL?limit=30&start=0" -o /tmp/p0.json
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "URL?limit=30&start=30" -o /tmp/p1.json
# ... continuar hasta que las fechas de la página sean anteriores al período buscado
```

```python
import json

# Cargar y combinar páginas
all_inv = []
for s in [0, 30, 60, ...]:
    d = json.load(open(f'/tmp/p_{s}.json'))
    if isinstance(d, list):
        all_inv.extend(d)

# Deduplicar por id
seen = set()
unique = [i for i in all_inv if not (i['id'] in seen or seen.add(i['id']))]

# Filtrar por fecha
filtrados = [i for i in unique if i['date'] == '2026-05-23']
```

## Clasificación de turnos

- **Mañana:** hora < 14 (facturas de 9:30 a 13:59)
- **Noche:** hora >= 17 (facturas de 17:30 a 21:xx)

```python
def turno(datetime_str):
    h = int(datetime_str[11:13])
    return 'Mañana' if h < 14 else 'Noche'
```

## Formato de respuesta

Siempre responder con:

1. **Resumen ejecutivo** — total facturado, cantidad de ventas, ticket promedio
2. **Tabla principal** con columnas relevantes al análisis pedido
3. **Observaciones** — destacar la venta más grande, patrones, anomalías si los hay

### Tabla de facturas individuales
| Hora | Total | Pago | Productos |
|---|---|---|---|

### Tabla de resumen por categoría (día/hora/medio de pago)
| Categoría | Facturas | Total | Prom/venta |
|---|---|---|---|

### Medios de pago
Mapear siempre: `cash`→Efectivo · `debit-card`→Débito · `transfer`→Transferencia · `credit-card`→Crédito

## Consultas frecuentes y cómo resolverlas

### "Ventas de hoy / ayer / esta semana / este mes"
Calculá la fecha desde `datetime` actual, traé suficientes páginas para cubrir el período, filtrá por fecha en Python y mostrá resumen + detalle.

### "Cómo fue la mañana / la tarde"
Filtrá por fecha de hoy y separar por turno (`hora < 14` = mañana, `hora >= 17` = noche).

### "Detalle de la factura X"
Buscá por `numberTemplate.formattedNumber == '0000XXXX'` en los datos ya cacheados en `/tmp/`. Si no está, traé más páginas.

### "Ventas del producto / referencia X"
Iterá sobre `i['items']` y filtrá donde `it.get('reference') == 'X'` o `it['name']` contiene el texto buscado.

### "Análisis por medio de pago"
Agrupar por `i['payments'][0]['paymentMethod']` y sumar totales.

### "Análisis por horario / ¿cuándo conviene abrir?"
Agrupar por `int(i['datetime'][11:13])` y calcular total y cantidad por franja. Dividir en turnos mañana/noche y por día de semana.

## Archivos temporales

Usar `/tmp/alegra_*.json` para páginas descargadas. Reutilizarlos si ya existen en la misma sesión para evitar llamadas redundantes a la API.

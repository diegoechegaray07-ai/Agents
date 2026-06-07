# Paginación y Filtrado Manual (Alegra API)

Este archivo detalla la lógica de paginación y filtrado si decides realizarla manualmente en lugar de usar el cliente compartido [`skills/_shared/alegra_client.py`](../_shared/alegra_client.py).

## Flujo de Trabajo en Consola
Puedes descargar las páginas usando `curl` y guardarlas en archivos temporales:

```bash
# Descargar las páginas secuencialmente cubriendo el período
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "URL?limit=30&start=0" -o /tmp/p0.json
curl -s -u "$ALEGRA_USER:$ALEGRA_TOKEN" "URL?limit=30&start=30" -o /tmp/p1.json
# ... repetir hasta que las fechas devueltas sean anteriores a tu fecha de interés.
```

## Lógica en Python
Para consolidar, deduplicar y filtrar las facturas en memoria:

```python
import json

# Lista para consolidar todas las facturas
all_inv = []
for s in [0, 30, 60, 90]:  # offsets
    try:
        with open(f'/tmp/p_{s}.json', 'r') as f:
            d = json.load(f)
            if isinstance(d, list):
                all_inv.extend(d)
    except FileNotFoundError:
        break

# Deduplicar facturas por ID único
seen = set()
unique = [i for i in all_inv if not (i['id'] in seen or seen.add(i['id']))]

# Filtrar por fecha exacta deseada (ejemplo: '2026-05-23')
filtrados = [i for i in unique if i['date'] == '2026-05-23']
```

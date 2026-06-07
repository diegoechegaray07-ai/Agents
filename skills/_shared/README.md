# Código compartido (`skills/_shared`)

Módulos reutilizables para no repetir lógica entre skills. Tienen tests en
[`tests/test_shared.py`](../../tests/test_shared.py).

| Módulo | Qué provee | Lo usan (o deberían) |
|---|---|---|
| `formatting.py` | `format_ars` (`$ 1.234,56`), `format_pct` | todos los informes |
| `alegra_client.py` | Cliente de Alegra: auth desde `.env`, paginación, filtrado por fecha en Python, mapeo de medios de pago, turnos | `alegra-api`, `reposicion-stock`, `cargar-factura-proveedor` |
| `pdf_brand.py` | Bloques de PDF de marca: paleta (cian `#03B0D6`), encabezado, tarjetas KPI, títulos de sección, tablas con total | `arca-informe`, `ddjj-iibb-san-juan`, `getnet-informe` |

## Cómo importarlo desde el script de una skill

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
from alegra_client import AlegraClient
from pdf_brand import Palette, kpi_row, data_table, section_title, draw_header_band
from formatting import format_ars
```

> Portabilidad: las skills son carpetas autocontenidas. Si copiás una skill que
> usa `_shared` a otro lado (ej. `~/.claude/skills/`), llevá también la carpeta
> `_shared`. `alegra_client` y los scripts traen fallbacks para degradar con
> elegancia si falta algo.

## Estado de adopción

Los módulos están listos y testeados. La migración de los scripts existentes
(que hoy reimplementan estas piezas) se hace **uno por uno, verificando la salida**
contra un archivo real antes de reemplazar. Empezar por el más simple.

## Credenciales

Nunca en el código. `alegra_client` lee `ALEGRA_USER` / `ALEGRA_TOKEN` del entorno
o de un `.env` (gitignored).

---
name: getnet-flujo-completo
description: >
  Flujo completo de Getnet: navegar el portal globalgetnet.com por Chrome,
  seleccionar uno o más establecimientos (DCG1, DCG2, etc.), descargar las
  transacciones en formato xlsx para un período dado (últimos 7 días por defecto),
  y generar informes PDF de ventas por cada establecimiento. Úsalo cuando el
  usuario diga "descargá las transacciones de Getnet", "hacé el informe de DCG1",
  "bajá el xlsx y generá el informe", "realizá el flujo completo de Getnet" o
  cualquier combinación de descarga + informe del portal Getnet. También aplica
  si el usuario solo pide la descarga sin informe, o solo el informe desde archivos
  ya subidos. IMPORTANTE: cuando el usuario diga "informe de domingo", ejecutar
  automáticamente este flujo para DCG1, DCG5, DCG7 y DCG9 (en ese orden).
---

# Skill: Flujo Completo Getnet

Automatiza el ciclo completo: **descarga xlsx desde el portal → generación de informe PDF**.

Para detalles del diseño y reglas del informe PDF, ver `references/reglas-informe.md`.

---

## Flujo de trabajo

```
1. CONECTAR al browser Chrome
2. NAVEGAR a portal.globalgetnet.com/s/transactions
3. CAMBIAR establecimiento (si no es el correcto)
4. VERIFICAR rango de fechas (últimos 7 días por defecto)
5. DESCARGAR xlsx
6. [Opcional] MOVER archivo a carpeta destino
7. GENERAR informe PDF desde el xlsx
8. PRESENTAR PDF al usuario
```

---

## PASO 1 — Conectar al browser

```python
# Siempre usar el browser Windows (25d73bab) para Getnet
# 1. list_connected_browsers → verificar disponibilidad
# 2. select_browser(deviceId)
# 3. tabs_context_mcp(createIfEmpty=True)
# 4. navigate a https://portal.globalgetnet.com/s/transactions
```

**Si la sesión expiró** (redirige a login):
- Avisar al usuario que ingrese sus credenciales
- Esperar confirmación ("listo") antes de continuar
- Luego navegar nuevamente a `/s/transactions`

**Permisos de dominio:**
- `portal.globalgetnet.com` ✅ permitido (usar siempre esta URL)
- `www.globalgetnet.com` ❌ sin permisos de extensión — nunca usarlo directamente

---

## PASO 2 — Seleccionar establecimiento

El portal carga el **último establecimiento usado**. Verificar el nombre en la esquina superior derecha.

Si no coincide con el solicitado:
1. Clic en el nombre del establecimiento (esquina superior derecha)
2. Clic en la flecha → "Mis establecimientos"
3. Hacer scroll si es necesario (DCG 6-9 quedan abajo)
4. Clic en el establecimiento correcto
5. Esperar que recargue (~5-8 seg)

**Establecimientos conocidos y sus propietarios para el informe:**

El mapeo establecimiento → propietario es **dato canónico** en
[references/establecimientos.json](references/establecimientos.json) (mismo archivo
que usa la skill `getnet-informe`). Consultá ahí el propietario para pasárselo al
script. Si el establecimiento no está en el JSON, usar el nombre tal cual.

---

## PASO 3 — Verificar período

El portal muestra el rango de fechas activo. Por defecto carga los **últimos 7 días**.

- Si el usuario no especificó período → usar el que está cargado (no modificar)
- Si el usuario pidió un período distinto → clic en el selector de fecha y ajustar

---

## PASO 4 — Descargar xlsx

1. **Activar monitor de red ANTES de descargar** (para capturar la URL):
   ```python
   read_network_requests(tabId=tab_id)  # activa el tracking
   ```
2. Clic en botón **Descargar** (esquina superior derecha)
3. Seleccionar **.xlsx** del menú desplegable
4. Esperar 5-8 segundos hasta que el menú se cierre
5. Capturar URL del xlsx desde network requests:
   ```python
   read_network_requests(filter_url='xlsx', tabId=tab_id)
   ```
6. Hacer fetch del contenido con javascript_tool y guardar en /tmp/

**Nota sobre carpeta destino:**
- Por defecto: carpeta de Descargas del navegador
- Si el usuario especificó una ruta (ej. `D:\OneDrive\...\Ayrton Gil`): Claude **no puede mover archivos** vía browser — indicar al usuario que configure esa carpeta como destino en `chrome://settings/downloads`

---

## PASO 5 — Generar informe PDF (automático, sin intervención del usuario)

**No pedir al usuario que suba el archivo.** Leerlo directamente desde el browser.

### Estrategia: capturar URL de descarga desde red y subir al chat

```python
# 1. Leer las network requests para encontrar la URL del xlsx descargado
#    usar read_network_requests en el tab activo

# 2. Hacer fetch del contenido como blob desde javascript_tool:
js_code = """
const url = '<URL_del_xlsx>';
const resp = await fetch(url);
const buf = await resp.arrayBuffer();
const b64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
return b64;
"""

# 3. Decodificar base64 y guardar en /tmp/ para procesarlo con el script
import base64
data = base64.b64decode(b64_content)
with open('/tmp/descarga.xlsx', 'wb') as f:
    f.write(data)

# 4. Ejecutar script de informe
python generar_informe.py /tmp/descarga.xlsx "<Propietario>" output.pdf
```

### Fallback: upload_image / file_upload tool
Si la URL no está disponible en red, usar `file_upload` para leer el archivo
desde el filesystem local del browser.

Ver `references/reglas-informe.md` para las reglas completas del informe.

---

## Informe de domingo (flujo automático)

Cuando el usuario diga **"informe de domingo"**, ejecutar automáticamente para:

| Orden | Establecimiento | Propietario |
|-------|----------------|-------------|
| 1°    | DCG 1          | Ayrton Gil  |
| 2°    | DCG 5          | Lucas Balmaceda |
| 3°    | DCG 7          | Jose Castro |
| 4°    | DCG 9          | Pets Company |

---

## Informe de miércoles (flujo automático)

Cuando el usuario diga **"informe de miércoles"**, ejecutar para:

| Orden | Establecimiento | Propietario |
|-------|----------------|-------------|
| 1°    | DCG 4          | Martin Costa |

---

## Informe de jueves (flujo automático)

Cuando el usuario diga **"informe de jueves"**, ejecutar para:

| Orden | Establecimiento | Propietario |
|-------|----------------|-------------|
| 1°    | DCG 2          | Jacqueline Muñoz |
| 2°    | DCG 8          | Sebastián Mas |

---

## Varios establecimientos

Si el usuario pide varios (ej. "DCG1 y DCG6"), repetir el ciclo descarga→informe
por cada uno: descargar DCG1 → confirmar → cambiar a DCG6 → descargar, leyendo
cada xlsx directamente del browser (PASO 5, sin pedir que los suban) y generar un
PDF por establecimiento. Presentar todos los PDF juntos al final.

---

## Manejo de errores frecuentes

| Problema | Solución |
|----------|----------|
| Screenshot timeout | Esperar 8-10 seg más y reintentar |
| Sesión expirada | Avisar al usuario, esperar login, navegar a `/s/transactions` |
| Browser desconectado | `list_connected_browsers` → `select_browser` → reintentar |
| Establecimiento incorrecto al cargar | Cambiar via selector antes de descargar |
| Permiso denegado en `www.globalgetnet.com` | Navegar directamente a `portal.globalgetnet.com/s/transactions` |

---

## Notas

- Siempre tomar screenshot para verificar cada paso clave
- El botón Descargar tiene un dropdown: `.csv` arriba, `.xlsx` abajo — hacer clic en `.xlsx`
- Después de cambiar de establecimiento, esperar que la página recargue completamente antes de descargar
- El encabezado del informe solo aparece en la primera página

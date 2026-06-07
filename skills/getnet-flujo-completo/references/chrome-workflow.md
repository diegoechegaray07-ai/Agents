# Flujo Técnico en Chrome (Getnet Automation)

Este archivo detalla las interacciones del navegador necesarias para conectar, cambiar de local, capturar peticiones de red y extraer el archivo `.xlsx` de transacciones sin solicitar al usuario que lo suba de forma manual.

---

## 1. Conexión Inicial y Navegación
1. Llama a `list_connected_browsers` para identificar las sesiones de Chrome disponibles.
2. Llama a `select_browser(deviceId)` utilizando la sesión preferida de Windows (`25d73bab`).
3. Llama a `tabs_context_mcp(createIfEmpty=True)` para asegurar una pestaña abierta.
4. Navega a `https://portal.globalgetnet.com/s/transactions`.
5. Si redirige a Login, consulta la guía de sesión expirada en [`references/manejo-errores.md`](manejo-errores.md).

---

## 2. Selección del Establecimiento
El portal de Getnet mantiene cargado por defecto el último establecimiento utilizado.
1. Revisa visualmente o mediante DOM el nombre en la esquina superior derecha.
2. Si no es el correcto, haz clic en el nombre actual del establecimiento.
3. Haz clic en la opción "Mis establecimientos".
4. Haz scroll en el menú desplegable si es necesario (los locales del DCG 6 al DCG 9 se encuentran más abajo).
5. Selecciona el local adecuado y espera a que el portal recargue los datos (~5 a 8 segundos).

---

## 3. Selector de Rango de Fechas
- Por defecto, el portal consulta los **últimos 7 días**.
- Si la petición de Diego no especifica fechas, utiliza este rango por defecto sin hacer modificaciones.
- Si Diego solicita un rango distinto (ej: "ventas de mayo"), haz clic sobre el selector de fecha del portal y ajusta los campos desde/hasta correspondientes.

---

## 4. Captura de Red y Descarga de `.xlsx`
Para descargar el archivo de datos sin que el usuario tenga que interactuar:
1. **Activa el monitor de red** antes de disparar la descarga:
   ```python
   read_network_requests(tabId=tab_id)
   ```
2. Haz clic en el botón **Descargar** en la esquina superior derecha de la página.
3. Selecciona **.xlsx** en el menú desplegable (es el segundo ítem, debajo de `.csv`).
4. Espera de 5 a 8 segundos a que se procese la descarga en segundo plano.
5. Captura la URL generada filtrando las solicitudes registradas:
   ```python
   read_network_requests(filter_url='xlsx', tabId=tab_id)
   ```
6. Descarga el contenido base64 ejecutando este bloque de Javascript mediante la herramienta del navegador:
   ```javascript
   const url = '<URL_del_xlsx_capturada>';
   const resp = await fetch(url);
   const buf = await resp.arrayBuffer();
   const b64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
   return b64;
   ```
7. Decodifica el base64 en Python y escribe el archivo en la ruta temporal para el script de generación del informe:
   ```python
   import base64
   data = base64.b64decode(b64_content)
   with open('/tmp/descarga.xlsx', 'wb') as f:
       f.write(data)
   ```
8. Finalmente, procesa el informe con el script del proyecto:
   ```bash
   python generar_informe.py /tmp/descarga.xlsx "<Propietario>" output.pdf
   ```

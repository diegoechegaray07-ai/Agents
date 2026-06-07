---
name: reposicion-stock
description: >-
  Asiste en la compra de mercadería de Pets Company cruzando el stock actual de Alegra con
  las ventas, compras y fraccionamientos reales de los últimos N días. Calcula los días de
  cobertura de cada artículo (stock ÷ ritmo de venta diario), distingue si conviene COMPRAR
  al proveedor o FRACCIONAR bolsas grandes que ya hay en stock, sugiere cuánto reponer y
  detecta fraccionamientos cuyos kilos no cuadran. Usalo SIEMPRE que el usuario pida:
  "qué tengo que comprar", "armá la lista de compra", "qué falta reponer", "análisis de
  stock", "qué se está por agotar", "alerta de stock", "días de cobertura", "informe de
  reposición", "qué pido al proveedor", o cualquier consulta sobre qué mercadería reabastecer.
  También aplica si el usuario quiere el PDF de alerta de stock o cruzar inventario con ventas.
---

# Reposición de stock — asistente de compra

Esta skill ejecuta el análisis de reposición de Pets Company y presenta los resultados de
forma accionable para decidir qué comprar. Toda la lógica pesada (consultar Alegra, calcular
cobertura, emparejar fraccionamientos) ya está implementada en un script del proyecto; tu
trabajo es correrlo con los parámetros adecuados e interpretar la salida para el usuario.

## Cómo funciona el cálculo (contexto)

Para cada artículo que maneja inventario:

- **consumo diario** = (unidades vendidas + salidas por ajuste/fraccionamiento) ÷ días efectivos de la ventana
- **días de cobertura** = stock actual ÷ consumo diario
- Se dispara alerta cuando la cobertura cae por debajo del umbral.
- **Origen de reposición**: si el artículo se viene reponiendo abriendo bolsas grandes
  (lo producido al fraccionar supera lo comprado), se marca **FRACCIONAR**; si no, **COMPRAR**.
- **Reponer** = unidades necesarias para cubrir los días objetivo del pedido.

Esto importa porque no todo lo que está bajo hay que comprarlo: muchos fraccionados de 1kg/½kg
se reponen abriendo una bolsa grande que ya está en depósito. Mezclar ambos lleva a comprar de más.

## Paso a paso

1. **Ubicá el proyecto.** El script vive en
   `tools/alerta_stock_bajo.py` dentro de la carpeta del proyecto Alegra Pets Company. Las
   credenciales de Alegra se leen solas del `.env` del proyecto, no hay que pasar nada.

2. **Elegí los parámetros** según lo que pida el usuario (ver tabla abajo). Si no aclara nada,
   usá los valores por defecto sugeridos.

3. **Ejecutá el script.** Es de ejecución larga (consulta cientos de facturas y ajustes), así
   que conviene correrlo en background y esperar a que termine antes de leer la salida:

   ```bash
   python3 tools/alerta_stock_bajo.py --ventana-dias 60 --dias-cobertura 21 --cobertura-objetivo 30 --pdf --no-snapshot
   ```

4. **Interpretá y presentá** los resultados con el formato de abajo. No vuelques la tabla cruda
   completa: agrupá y priorizá para que sea útil al momento de comprar.

## Parámetros

| Flag | Qué controla | Default sugerido | Cuándo cambiarlo |
|------|--------------|------------------|------------------|
| `--ventana-dias` | Días hacia atrás para medir el ritmo de venta | 60 | Más corto (30) si hubo cambios fuertes de demanda recientes; más largo (90) para suavizar estacionalidad |
| `--dias-cobertura` | Umbral: alerta si quedan menos de N días | 21 | Bajalo (14) para ver solo lo urgente; subilo (30) para planificar con anticipación |
| `--cobertura-objetivo` | Días que debe cubrir el pedido sugerido | 30 | Ajustá según frecuencia de compra al proveedor |
| `--pdf` | Genera además el PDF con estilo de marca en `data/alertas/` | usar | Omitir si solo se quiere el resumen en pantalla |
| `--no-snapshot` | No guardar la foto de stock del día en el historial | — | Por defecto, en una corrida real (no de prueba) **dejá que guarde el snapshot** (no pongas este flag) para construir historial |

> Nota sobre el snapshot: el script guarda una foto diaria del stock en `data/stock_history.json`.
> En corridas reales conviene dejar que la guarde (omitir `--no-snapshot`) para tener historial.
> Usá `--no-snapshot` solo en pruebas o si vas a correrlo varias veces el mismo día.

## Lista de compra en PDF (por marca, con costo)

Cuando el usuario pida **exportar la lista de compra**, "armá la lista para el proveedor",
"pasame el pedido en PDF" o similar, usá el script `tools/gen_lista_compra_pdf.py`. Reutiliza
el mismo análisis de reposición (incluido el mapa de semillas), filtra solo los **COMPRAR** y
genera dos PDF con estilo de marca, agrupados por marca, con **subtotal de costo por marca** y
**total estimado a invertir** (costo = cantidad a pedir × costo unitario de Alegra):

```bash
python3 tools/gen_lista_compra_pdf.py            # genera ambos PDF (completo + solo alimento)
python3 tools/gen_lista_compra_pdf.py --solo-alimento   # solo alimento + semillas (sin accesorios)
python3 tools/gen_lista_compra_pdf.py --completa        # solo el PDF completo
```

Acepta los mismos `--ventana-dias`, `--dias-cobertura` y `--cobertura-objetivo`. Los PDF se
guardan en la raíz del proyecto como `Lista_Compra_<fecha>.pdf` y `Lista_Compra_Alimento_<fecha>.pdf`.
Es de ejecución larga (consulta Alegra), correlo en background.

## Formato de presentación

Después de correr el script, presentá un resumen accionable, no la tabla cruda. Estructura:

### 1. Resumen general
Cantidad de artículos analizados y total de alertas, desglosado en: sin stock, a comprar, a fraccionar.
Mencioná la ruta del PDF generado.

### 2. 🔴 Prioridad máxima — COMPRAR ya
Artículos con origen COMPRAR, **sin stock** y con ventas en la ventana (los que rotan y están en cero).
Tabla con: artículo, vendidos en la ventana, cuánto reponer.

### 3. 🟡 Bolsas/productos a comprar que se están por agotar
Resto de los COMPRAR con stock bajo pero > 0, ordenados por días de cobertura ascendente.

### 4. 🔵 No comprar — FRACCIONAR
Artículos bajos que se reponen abriendo bolsas grandes ya en stock. Listalos para que NO se
compren de más, aclarando que se cubren fraccionando.

### 5. ⚠️ Fraccionamientos que no cuadran por peso
Si el script reporta descuadres, listalos: son posibles errores de carga de inventario que
distorsionan el stock real y conviene revisar.

### 6. Cierre
Ofrecé acciones de seguimiento: abrir el PDF, ajustar parámetros (ventana, umbral, objetivo),
o armar una lista de compra limpia agrupada por marca/proveedor para enviar al proveedor.

## Fraccionamiento de semillas (mapa de equivalencias)

Las semillas y granos (alpiste, girasol, mijo, mezcla pico duro, conejo, pollito bebé) se
venden fraccionadas en 1kg y ½kg, pero ese fraccionamiento **no se registra como ajuste de
inventario en Alegra** y los nombres de bulto y fracción difieren, así que el emparejamiento
automático por ajustes no las detecta. Para resolverlo, el archivo
`tools/fraccionamiento_semillas.json` define el mapa **bulto madre → fracciones** (con sus kg).

El tool lo usa para:
1. Forzar las fracciones de semillas a **FRACCIONAR** (no se compran sueltas).
2. Sumar la demanda de las fracciones (convertida a kg → unidades de bulto) al consumo del
   **bulto madre**, de modo que la cantidad a COMPRAR del bulto contemple lo que se vende fraccionado.

Si aparece una semilla nueva o cambia una equivalencia, editá ese JSON (no hace falta tocar el
código). Ojo: hay productos que parecen fracción pero se compran armados (ej. Alpiste c/Vitaminas);
esos NO van en el mapa y quedan como COMPRAR.

## Consejos

- Si el usuario pide "lista de compra para el proveedor", filtrá solo los COMPRAR y agrupá por
  marca (Old Prince, Royal Canin, Pedigree, etc.), sumando las cantidades a reponer.
- Si pide "solo lo urgente", corré con `--dias-cobertura 14` o filtrá los de cobertura 0.
- El ritmo de venta ya descuenta correctamente el fraccionamiento, así que confiá en la columna
  Reponer; no la recalcules a mano.
- Las unidades de bolsas grandes que aparecen como FRACCIONAR igualmente pueden necesitar compra
  si el stock de la bolsa madre también está bajo: revisá la bolsa grande correspondiente.

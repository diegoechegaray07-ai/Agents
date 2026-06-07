# Edición local — `imgtool.py`

Motor por defecto: Pillow. Determinista, offline, reproducible. Corré los
subcomandos desde la carpeta de la skill. Toda salida se borra antes de
recrearse (gotcha OneDrive).

## Subcomandos

| Comando | Qué hace | Flags clave |
|---|---|---|
| `info` | dims, modo, formato, peso | acepta varios archivos |
| `resize` | redimensiona | `--width --height --pct --aspect --fit cover\|contain\|stretch --pad` |
| `convert` | cambia formato por extensión de salida | `--quality` |
| `compress` | baja peso | `--target-kb N` (busca calidad por bisección) o `--quality` |
| `crop` | recorta | `--box x,y,w,h` o `--aspect W:H` (centrado) |
| `rotate` | rota horario | `--deg` `--expand` |
| `flip` | espeja | `--axis h\|v` |
| `pad` | encaja en lienzo (letterbox) | `--size 1080x1080 --color` |
| `thumb` | miniatura cuadrada | `--size` |
| `watermark` | marca de agua texto/logo | `--text` o `--logo`, `--pos`, `--opacity`, `--scale` |
| `grid` | collage en grilla | `--inputs a,b,c --cols --cell --gap --bg` |
| `palette` | colores dominantes (hex) | `--colors` |
| `round` | esquinas redondeadas (PNG) | `--radius` |
| `removebg` | quita fondo (necesita `rembg`) | — |
| `filter` | blur/sharpen/grayscale/contour/smooth/edge | `--amount` |

Posición de marca de agua (`--pos`): primera letra vertical (`t`/`m`/`b`),
segunda horizontal (`l`/`c`/`r`). Ej: `br` abajo-derecha, `tl` arriba-izquierda.

## Formatos de salida

La extensión define el formato. JPG/PDF se aplanan a RGB automáticamente; PNG y
WebP conservan transparencia. Para web preferí WebP (mejor relación peso/calidad).

## Tamaños canónicos útiles (placas de redes)

| Destino | Tamaño (px) | Aspecto |
|---|---|---|
| Instagram post cuadrado | 1080×1080 | 1:1 |
| Instagram retrato | 1080×1350 | 4:5 |
| Story / Reel / TikTok | 1080×1920 | 9:16 |
| Portada de Facebook | 1640×856 | ~1.91:1 |
| Miniatura YouTube | 1280×720 | 16:9 |
| WhatsApp estado | 1080×1920 | 9:16 |

Si dudás de un tamaño actual, verificá con `WebSearch` antes de componer.

## Cuando el script no alcanza

Si el pedido es una transformación que no está cubierta, escribí Pillow ad-hoc
imitando los patrones de [scripts/imgtool.py](../scripts/imgtool.py): usá
`_safe_save` (borrar antes de guardar), `ImageOps.fit` para recortes que llenan,
`alpha_composite` para superponer con transparencia. No hagas la edición a mano
paso a paso: codificala para que sea reproducible.

## Dependencias

- `rembg` (quitar fondo): **instalado** (con `rembg[cpu]`/onnxruntime). El modelo
  u2net vive en `C:\Users\Diego\.u2net\`; corre offline. `removebg` ya funciona.
- ImageMagick (`magick`): no instalado. Pillow cubre casi todo; solo ofrecelo
  para casos exóticos (animaciones complejas, conversiones raras).

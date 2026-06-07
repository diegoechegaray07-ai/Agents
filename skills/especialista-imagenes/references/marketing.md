# Gráfica de marketing (carteles, flyers, placas, stickers)

Dos caminos según cuánto control y reproducibilidad querés:

- **Composición local con Pillow** — control pixel-perfect, reproducible por
  código, imprimible (PDF/PNG a DPI fijo). Es el patrón que ya usa la skill
  `qr-pets-company` (mirá `scripts/regenerar.py` de ese proyecto como modelo).
- **Canva** — terminación profesional rápida con plantillas y marca. Ver
  [canva.md](canva.md).

## Patrón de composición local

1. **Lienzo** del tamaño/aspecto del destino (ver tabla en
   [edicion-local.md](edicion-local.md)). Para imprenta, calculá px = cm × DPI/2.54
   (usá 300 DPI para impresión, 72–150 para pantalla).
2. **Fondo**: color sólido, degradé, o imagen pasada por `imgtool.py resize
   --fit cover`.
3. **Capas**: logo, textos, QR, formas. Componé con `ImageDraw` y
   `alpha_composite`. Cargá fuentes del sistema (`C:/Windows/Fonts/...`) o de
   `assets/`.
4. **Jerarquía visual**: un titular grande, un subtítulo, un llamado a la acción.
   Respetá márgenes (≈3–5% del lado menor) y contraste texto/fondo.
5. **Exportar**: PNG para pantalla, PDF para imprimir (Pillow guarda PDF desde
   RGB). Para multipágina o A4 exacto, mirá `cartel_a4_pdf.py` del proyecto QR.

Cristalizá el diseño en un script con parámetros (textos, colores, rutas) para
poder regenerarlo sin rehacerlo. Si se vuelve recurrente, convertilo en sub-skill
(ver [crear-subskill.md](crear-subskill.md)).

## Identidad de marca

Antes de componer, fijá: paleta, tipografías y logo en alta, y reusá esos valores
en todas las piezas. Para **Pet's Company** ya hay un kit armado (logos
transparentes + paleta cian `#03B0D6`): ver [kit-marca.md](kit-marca.md) y
`scripts/brandkit.py stamp`. Para otra marca, extraé la paleta con
`imgtool.py palette` y, si conviene, armá su kit con `brandkit.py build`.

## Buenas prácticas rápidas

- Texto siempre legible: alto contraste, evitá texto sobre zonas ruidosas de una
  foto (usá una capa semitransparente detrás).
- Exportá a las dimensiones nativas de cada red; no estires.
- Guardá el editable/script; entregá el render.

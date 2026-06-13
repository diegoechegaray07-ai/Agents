# Kit de marca

Cada marca vive en `assets/brand/<marca>/` con un `brand.json` (paleta, rutas de
logos, tipografía) y los logos en PNG **con fondo transparente** (celeste y
blanco). Generados por `scripts/brandkit.py` desde los JPG originales.

## Pet's Company (`petscompany`) — ya armado

- **Color de marca**: cian `#03B0D6` (rgb 3,176,214). Secundario claro `#9EE0EC`.
- **Tagline**: "Especialistas en tu mascota".
- **Logos** (en `assets/brand/petscompany/`, transparentes): `icono`, `vertical`
  y `horizontal`, cada uno en `_celeste.png` y `_blanco.png`.
  - Usá la variante **blanca** sobre fondos celestes/oscuros, la **celeste**
    sobre blanco/claros.
- **Tipografía**: titular serif slab (estilo Rockwell; fallback Georgia/Times),
  tagline sans mayúscula con tracking amplio (fallback Arial/Segoe). Si conseguís
  la fuente exacta, dejala en `assets/brand/fonts/`.

Leé `assets/brand/petscompany/brand.json` para las rutas y colores exactos antes
de componer una pieza.

## Estampar el logo sobre una imagen

```
python scripts/brandkit.py stamp entrada.jpg salida.png --logo icono_celeste --pos br --scale 16
python scripts/brandkit.py stamp placa.png  out.png    --logo horizontal_blanco --pos bc --scale 40
```

`--logo` = clave de `brand.json` (icono/vertical/horizontal × celeste/blanco).
`--pos` t/m/b + l/c/r. `--scale` % del ancho de la base.

## Regenerar el kit (si cambian los logos)

```
python scripts/brandkit.py build --brand petscompany --src "<carpeta con los JPG>"
```

Los originales de Pet's Company están en
`D:\OneDrive\DCG y ROE - Diego\Diego\Pets Company\logopetscompany`.
`build` recolorea por color-key sobre fondo sólido (arte monocolor), así que
funciona para cualquier logo de un solo color sobre fondo plano.

## Componer una placa con identidad

1. Leé `brand.json` → paleta y logo.
2. Lienzo del tamaño de la red (ver [edicion-local.md](edicion-local.md)).
3. Fondo en color de marca o blanco; texto en la tipografía/colores del kit.
4. Estampá el logo con `brandkit.py stamp` o componé con Pillow.
5. Para piezas recurrentes (placas fijas de un negocio), cristalizá en sub-skill
   ([crear-subskill.md](crear-subskill.md)). Modelo: `qr-pets-company`.

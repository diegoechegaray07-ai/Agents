#!/usr/bin/env python3
"""brandkit — genera y aplica el kit de marca (logos transparentes + sello).

`build`  reconstruye las variantes PNG con fondo transparente desde los JPG
         monocolor del logo (color-key sobre fondo solido).
`stamp`  estampa un logo de la marca sobre una imagen/placa.

El kit vive en assets/brand/<marca>/ con un brand.json (paleta, rutas, fuentes).
"""
import argparse
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(os.path.dirname(HERE), "assets", "brand")


def _safe_save(img, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
    img.save(path)
    print(f"OK -> {os.path.relpath(path, BRAND_DIR)} ({img.size[0]}x{img.size[1]})")


def color_to_alpha(im, bg, tint=None, thresh=12):
    """Vuelve transparente el fondo solido `bg`. Si `tint`, recolorea la tinta.

    Asume arte monocolor sobre fondo plano. alpha se estima por la distancia
    del pixel al color de fondo (0 = es fondo, 255 = tinta plena)."""
    im = im.convert("RGB")
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    br, bgc, bb = bg
    # canal con mayor contraste fondo<->tinta para estimar alpha
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = max(abs(r - br), abs(g - bgc), abs(b - bb))
            if d <= thresh:
                continue
            a = min(255, int(d / (255 - min(br, bgc, bb) + 1e-6) * 255)) if min(br, bgc, bb) < 200 \
                else min(255, int((255 - min(r, g, b)) / (255 - 3) * 255))
            if tint:
                op[x, y] = (tint[0], tint[1], tint[2], a)
            else:
                op[x, y] = (r, g, b, a)
    return out


# fuentes (nombre logico -> archivo JPG de origen, fondo, marca)
SOURCES = {
    "icono": "Pet Company Icon Fondo Blanco.jpg",
    "vertical": "Pet Company Logo Fondo Blanco.jpg",
    "horizontal": "Pet Company Logo Horizontal Fondo Blanco.jpg",
}
WHITE = (255, 255, 255)
CYAN = (3, 176, 214)


def cmd_build(a):
    src = os.path.abspath(a.src)
    if not os.path.isdir(src):
        sys.exit(f"build: no existe la carpeta de origen {src}")
    out = os.path.join(BRAND_DIR, a.brand)
    for name, fname in SOURCES.items():
        fpath = os.path.join(src, fname)
        if not os.path.exists(fpath):
            print(f"  (falta {fname}, salteo {name})")
            continue
        im = Image.open(fpath)
        # variante celeste sobre transparente (desde fondo blanco)
        cyan = color_to_alpha(im, WHITE)
        _safe_save(cyan, os.path.join(out, f"{name}_celeste.png"))
        # variante blanca sobre transparente (recolorea la tinta a blanco)
        white = color_to_alpha(im, WHITE, tint=WHITE)
        _safe_save(white, os.path.join(out, f"{name}_blanco.png"))
    # brand.json
    brand = {
        "nombre": "Pet's Company",
        "tagline": "Especialistas en tu mascota",
        "colores": {
            "celeste": "#03B0D6",
            "celeste_rgb": [3, 176, 214],
            "blanco": "#FFFFFF",
            "celeste_claro": "#9EE0EC",
        },
        "logos": {
            "icono_celeste": f"{a.brand}/icono_celeste.png",
            "icono_blanco": f"{a.brand}/icono_blanco.png",
            "vertical_celeste": f"{a.brand}/vertical_celeste.png",
            "vertical_blanco": f"{a.brand}/vertical_blanco.png",
            "horizontal_celeste": f"{a.brand}/horizontal_celeste.png",
            "horizontal_blanco": f"{a.brand}/horizontal_blanco.png",
        },
        "tipografia": {
            "titular": "serif slab (estilo Rockwell); fallback Georgia/Times",
            "tagline": "sans mayuscula con tracking amplio; fallback Arial/Segoe",
            "nota": "si tenes la fuente exacta, dejala en assets/brand/fonts/",
        },
        "origen": src,
    }
    bpath = os.path.join(out, "brand.json")
    os.makedirs(out, exist_ok=True)
    if os.path.exists(bpath):
        os.remove(bpath)
    with open(bpath, "w", encoding="utf-8") as f:
        json.dump(brand, f, ensure_ascii=False, indent=2)
    print(f"OK -> {a.brand}/brand.json")


def cmd_stamp(a):
    """Estampa el logo de la marca sobre una imagen (esquina o centrado)."""
    brand_json = os.path.join(BRAND_DIR, a.brand, "brand.json")
    if not os.path.exists(brand_json):
        sys.exit(f"stamp: falta el kit. Corré primero: brandkit.py build --brand {a.brand} --src <carpeta>")
    brand = json.load(open(brand_json, encoding="utf-8"))
    logo_rel = brand["logos"].get(a.logo)
    if not logo_rel:
        sys.exit(f"stamp: logo '{a.logo}' no existe. Opciones: {', '.join(brand['logos'])}")
    base = Image.open(os.path.abspath(a.input)).convert("RGBA")
    logo = Image.open(os.path.join(BRAND_DIR, logo_rel)).convert("RGBA")
    lw = int(base.width * a.scale / 100)
    logo.thumbnail((lw, lw * 4), Image.LANCZOS)
    m = int(min(base.size) * 0.04)
    x = {"l": m, "c": (base.width - logo.width) // 2, "r": base.width - logo.width - m}[a.pos[1]]
    y = {"t": m, "m": (base.height - logo.height) // 2, "b": base.height - logo.height - m}[a.pos[0]]
    base.alpha_composite(logo, (x, y))
    out = os.path.abspath(a.output)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if os.path.exists(out):
        os.remove(out)
    if out.lower().endswith((".jpg", ".jpeg")):
        base = base.convert("RGB")
    base.save(out)
    print(f"OK -> {out} ({base.size[0]}x{base.size[1]})")


def build_parser():
    p = argparse.ArgumentParser(description="Kit de marca: logos transparentes + sello.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("build", help="genera variantes transparentes + brand.json")
    s.add_argument("--brand", default="petscompany")
    s.add_argument("--src", required=True, help="carpeta con los JPG del logo")
    s.set_defaults(func=cmd_build)

    s = sub.add_parser("stamp", help="estampa un logo de la marca sobre una imagen")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--brand", default="petscompany")
    s.add_argument("--logo", default="icono_celeste", help="clave de logos en brand.json")
    s.add_argument("--pos", default="br", help="t/m/b + l/c/r")
    s.add_argument("--scale", type=float, default=18, help="%% del ancho base")
    s.set_defaults(func=cmd_stamp)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)

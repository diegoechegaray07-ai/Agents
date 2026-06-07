#!/usr/bin/env python3
"""compose — mockups y PDF multipagina con Pillow.

Mismo contrato que imgtool.py: la salida se borra antes de recrearse (gotcha
OneDrive). Se invoca desde el SKILL.md, no se carga su codigo en contexto.

    python compose.py mockup foto.png out.png --type phone
    python compose.py pdf catalogo.pdf --inputs a.jpg,b.jpg,c.jpg --page a4
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageOps


def _safe_save(img, path, **kw):
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        img = img.convert("RGB")
    img.save(path, **kw)
    print(f"OK -> {path} ({img.size[0]}x{img.size[1]})")


def _open(p):
    return Image.open(os.path.abspath(p))


def _parse_color(s):
    if s and "," in s:
        return tuple(int(x) for x in s.split(","))
    return s


def _rounded(im, rad):
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), rad, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def _shadow(size, rad, blur, color=(0, 0, 0, 120)):
    from PIL import ImageFilter
    pad = blur * 3
    sh = Image.new("RGBA", (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (pad, pad, pad + size[0], pad + size[1]), rad, fill=color)
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad


# ---------------------------------------------------------------- mockup
def cmd_mockup(a):
    """Inserta la imagen en un marco generado proceduralmente."""
    src = _open(a.input).convert("RGB")
    bg = _parse_color(a.bg) or (235, 235, 238)

    if a.type == "phone":
        # cuerpo de telefono 9:19.5 con pantalla redondeada
        screen = ImageOps.fit(src, (900, 1950), Image.LANCZOS)
        body_pad, rad = 60, 120
        body = Image.new("RGBA", (screen.width + body_pad * 2,
                                  screen.height + body_pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(body).rounded_rectangle(
            (0, 0, body.width, body.height), rad + body_pad, fill=(20, 20, 24, 255))
        body.alpha_composite(_rounded(screen, rad), (body_pad, body_pad))
        device = body
    elif a.type == "browser":
        # ventana de navegador con barra y tres puntos
        win = ImageOps.fit(src, (1600, 900), Image.LANCZOS)
        bar = 70
        device = Image.new("RGBA", (win.width, win.height + bar), (245, 245, 247, 255))
        d = ImageDraw.Draw(device)
        d.rectangle((0, 0, device.width, bar), fill=(228, 228, 232, 255))
        for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            d.ellipse((24 + i * 34, bar // 2 - 9, 24 + i * 34 + 18, bar // 2 + 9), fill=col)
        device.paste(win, (0, bar))
        device = _rounded(device, 24)
    else:  # frame / cuadro: passepartout blanco + borde
        mat = 80
        framed = ImageOps.expand(src, border=mat, fill=(255, 255, 255))
        framed = ImageOps.expand(framed, border=28, fill=(30, 30, 30))
        device = framed.convert("RGBA")

    # componer sobre fondo con sombra
    margin = int(max(device.size) * 0.12)
    canvas = Image.new("RGBA", (device.width + margin * 2,
                                device.height + margin * 2), bg + (255,) if isinstance(bg, tuple) else bg)
    if not a.no_shadow:
        sh, pad = _shadow(device.size, 80, 40)
        canvas.alpha_composite(sh, (margin - pad, margin - pad + 20))
    canvas.alpha_composite(device, (margin, margin))
    _safe_save(canvas.convert("RGB") if a.output.lower().endswith((".jpg", ".jpeg")) else canvas,
               a.output)


# ---------------------------------------------------------------- pdf
A4_PORTRAIT = (1654, 2339)   # ~200 DPI
A4_LANDSCAPE = (2339, 1654)


def cmd_pdf(a):
    paths = [p.strip() for p in a.inputs.split(",") if p.strip()]
    if not paths:
        sys.exit("pdf: pasá --inputs con al menos una imagen")
    margin = a.margin
    bg = _parse_color(a.bg) or "white"
    pages = []
    for p in paths:
        im = _open(p).convert("RGB")
        if a.page == "native":
            page = im
        else:
            canvas_size = A4_LANDSCAPE if a.page == "a4-landscape" else A4_PORTRAIT
            page = Image.new("RGB", canvas_size, bg)
            area = (canvas_size[0] - margin * 2, canvas_size[1] - margin * 2)
            fitted = im.copy()
            fitted.thumbnail(area, Image.LANCZOS)
            page.paste(fitted, ((canvas_size[0] - fitted.width) // 2,
                                (canvas_size[1] - fitted.height) // 2))
        pages.append(page)
    out = os.path.abspath(a.output)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if os.path.exists(out):
        os.remove(out)
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=200)
    print(f"OK -> {out} ({len(pages)} paginas)")


# ---------------------------------------------------------------- parser
def build_parser():
    p = argparse.ArgumentParser(description="Mockups y PDF multipagina (Pillow).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("mockup", help="insertar imagen en un marco (phone/browser/frame)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--type", choices=["phone", "browser", "frame"], default="frame")
    s.add_argument("--bg", default="235,235,238", help="color de fondo")
    s.add_argument("--no-shadow", action="store_true")
    s.set_defaults(func=cmd_mockup)

    s = sub.add_parser("pdf", help="combinar imagenes en un PDF multipagina")
    s.add_argument("output")
    s.add_argument("--inputs", required=True, help="rutas separadas por coma (orden = paginas)")
    s.add_argument("--page", choices=["a4", "a4-landscape", "native"], default="a4")
    s.add_argument("--margin", type=int, default=80)
    s.add_argument("--bg", default="white")
    s.set_defaults(func=cmd_pdf)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)

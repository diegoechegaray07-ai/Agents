#!/usr/bin/env python3
"""imgtool — operaciones deterministas sobre imagenes con Pillow.

Cada subcomando hace una transformacion frecuente. La salida se BORRA antes de
recrearse para esquivar el OSError [Errno 22] de PIL al sobrescribir placeholders
de OneDrive. Diseñado para correr sin cargar su codigo en contexto: el SKILL.md
solo lo invoca.

Uso general:
    python imgtool.py <comando> [args] [--flags]
    python imgtool.py --help          # lista comandos
    python imgtool.py <comando> -h    # ayuda del comando
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter


# ---------------------------------------------------------------- helpers
def _safe_save(img, path, **kw):
    """Borra el destino antes de guardar (gotcha OneDrive) y crea carpetas."""
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img = img.convert("RGB")
        kw.setdefault("quality", 90)
        kw.setdefault("optimize", True)
    elif ext == ".webp":
        kw.setdefault("quality", 90)
    elif ext == ".pdf":
        img = img.convert("RGB")
    img.save(path, **kw)
    print(f"OK -> {path} ({img.size[0]}x{img.size[1]})")


def _open(path):
    return Image.open(os.path.abspath(path))


def _parse_aspect(s):
    a, b = s.replace(":", "/").split("/")
    return float(a) / float(b)


def _parse_color(s):
    if s is None:
        return None
    if "," in s:  # "255,255,255" o "255,255,255,0"
        return tuple(int(x) for x in s.split(","))
    return s  # nombre o #hex


def _load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except OSError:
            continue
    return ImageFont.load_default()


# ---------------------------------------------------------------- comandos
def cmd_info(a):
    for p in a.inputs:
        im = _open(p)
        kb = os.path.getsize(os.path.abspath(p)) / 1024
        print(f"{p}: {im.format} {im.mode} {im.size[0]}x{im.size[1]} {kb:.0f}KB")


def cmd_resize(a):
    im = _open(a.input)
    w, h = im.size
    if a.pct:
        tw, th = int(w * a.pct / 100), int(h * a.pct / 100)
    else:
        tw, th = a.width, a.height
    if a.aspect and (tw or th):
        ar = _parse_aspect(a.aspect)
        if tw and not th:
            th = int(tw / ar)
        elif th and not tw:
            tw = int(th * ar)
    if not tw and th:
        tw = int(w * th / h)
    if not th and tw:
        th = int(h * tw / w)

    if a.fit == "cover":
        out = ImageOps.fit(im, (tw, th), method=Image.LANCZOS)
    elif a.fit == "contain":
        out = im.copy()
        out.thumbnail((tw, th), Image.LANCZOS)
        if a.pad:
            bg = Image.new(im.mode, (tw, th), _parse_color(a.pad))
            bg.paste(out, ((tw - out.width) // 2, (th - out.height) // 2))
            out = bg
    else:  # stretch
        out = im.resize((tw, th), Image.LANCZOS)
    _safe_save(out, a.output)


def cmd_convert(a):
    im = _open(a.input)
    kw = {}
    if a.quality:
        kw["quality"] = a.quality
    _safe_save(im, a.output, **kw)


def cmd_compress(a):
    im = _open(a.input).convert("RGB")
    if a.target_kb:
        lo, hi, best = 10, 95, None
        for _ in range(8):  # busqueda binaria de calidad
            q = (lo + hi) // 2
            import io
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=q, optimize=True)
            kb = buf.tell() / 1024
            if kb <= a.target_kb:
                best = q
                lo = q + 1
            else:
                hi = q - 1
        _safe_save(im, a.output, quality=best or 10, optimize=True)
    else:
        _safe_save(im, a.output, quality=a.quality or 75, optimize=True)


def cmd_crop(a):
    im = _open(a.input)
    if a.box:
        x, y, w, h = (int(v) for v in a.box.split(","))
        out = im.crop((x, y, x + w, y + h))
    elif a.aspect:
        ar = _parse_aspect(a.aspect)
        w, h = im.size
        if w / h > ar:  # demasiado ancha
            nw = int(h * ar)
            x = (w - nw) // 2
            out = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / ar)
            y = (h - nh) // 2
            out = im.crop((0, y, w, y + nh))
    else:
        sys.exit("crop: pasá --box x,y,w,h o --aspect W:H")
    _safe_save(out, a.output)


def cmd_rotate(a):
    im = _open(a.input)
    out = im.rotate(-a.deg, expand=a.expand, resample=Image.BICUBIC)
    _safe_save(out, a.output)


def cmd_flip(a):
    im = _open(a.input)
    out = ImageOps.mirror(im) if a.axis == "h" else ImageOps.flip(im)
    _safe_save(out, a.output)


def cmd_pad(a):
    im = _open(a.input)
    tw, th = (int(v) for v in a.size.lower().split("x"))
    out = ImageOps.pad(im, (tw, th), color=_parse_color(a.color) or "white",
                       method=Image.LANCZOS)
    _safe_save(out, a.output)


def cmd_thumb(a):
    im = _open(a.input)
    out = im.copy()
    out.thumbnail((a.size, a.size), Image.LANCZOS)
    _safe_save(out, a.output)


def cmd_watermark(a):
    im = _open(a.input).convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    margin = int(min(im.size) * 0.03)
    if a.logo:
        logo = _open(a.logo).convert("RGBA")
        lw = int(im.width * (a.scale or 18) / 100)
        logo.thumbnail((lw, lw), Image.LANCZOS)
        if a.opacity < 100:
            alpha = logo.split()[3].point(lambda p: int(p * a.opacity / 100))
            logo.putalpha(alpha)
        pos = _wm_pos(a.pos, im.size, logo.size, margin)
        overlay.alpha_composite(logo, pos)
    else:
        fs = int(min(im.size) * (a.scale or 5) / 100)
        font = _load_font(fs, bold=True)
        bbox = draw.textbbox((0, 0), a.text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos = _wm_pos(a.pos, im.size, (tw, th), margin)
        alpha = int(255 * a.opacity / 100)
        draw.text(pos, a.text, font=font, fill=(255, 255, 255, alpha),
                  stroke_width=max(1, fs // 20), stroke_fill=(0, 0, 0, alpha))
    out = Image.alpha_composite(im, overlay)
    _safe_save(out, a.output)


def _wm_pos(pos, base, item, m):
    bw, bh = base
    iw, ih = item
    x = {"l": m, "c": (bw - iw) // 2, "r": bw - iw - m}[pos[1] if len(pos) > 1 else "r"]
    y = {"t": m, "m": (bh - ih) // 2, "b": bh - ih - m}[pos[0]]
    return (x, y)


def cmd_grid(a):
    paths = [p.strip() for p in a.inputs.split(",") if p.strip()]
    imgs = [_open(p) for p in paths]
    cols = a.cols
    rows = (len(imgs) + cols - 1) // cols
    cell = a.cell
    gap = a.gap
    bg = _parse_color(a.bg) or "white"
    W = cols * cell + (cols + 1) * gap
    H = rows * cell + (rows + 1) * gap
    canvas = Image.new("RGB", (W, H), bg)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        tile = ImageOps.fit(im.convert("RGB"), (cell, cell), Image.LANCZOS)
        x = gap + c * (cell + gap)
        y = gap + r * (cell + gap)
        canvas.paste(tile, (x, y))
    _safe_save(canvas, a.output)


def cmd_palette(a):
    im = _open(a.input).convert("RGB")
    small = im.copy()
    small.thumbnail((200, 200))
    q = small.quantize(colors=a.colors, method=Image.FASTOCTREE)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    print(f"Paleta dominante de {a.input}:")
    for cnt, idx in counts[: a.colors]:
        r, g, b = pal[idx * 3:idx * 3 + 3]
        pct = 100 * cnt / (small.width * small.height)
        print(f"  #{r:02X}{g:02X}{b:02X}  rgb({r},{g},{b})  {pct:4.1f}%")


def cmd_round(a):
    im = _open(a.input).convert("RGBA")
    rad = a.radius
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, im.width, im.height), radius=rad, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    _safe_save(out, a.output)


def cmd_removebg(a):
    try:
        from rembg import remove
    except ImportError:
        sys.exit("removebg: falta 'rembg'. Instalalo con: pip install rembg\n"
                 "Alternativa: usá Canva (ver references/canva.md).")
    data = remove(_open(a.input))
    _safe_save(data, a.output)


def cmd_filter(a):
    im = _open(a.input)
    fmap = {
        "blur": ImageFilter.GaussianBlur(a.amount or 4),
        "sharpen": ImageFilter.UnsharpMask(),
        "contour": ImageFilter.CONTOUR,
        "smooth": ImageFilter.SMOOTH_MORE,
        "edge": ImageFilter.FIND_EDGES,
    }
    if a.name == "grayscale":
        out = ImageOps.grayscale(im)
    elif a.name in fmap:
        out = im.filter(fmap[a.name])
    else:
        sys.exit(f"filter: desconocido '{a.name}'. Opciones: {', '.join(list(fmap)+['grayscale'])}")
    _safe_save(out, a.output)


# ---------------------------------------------------------------- parser
def build_parser():
    p = argparse.ArgumentParser(description="Operaciones deterministas sobre imagenes (Pillow).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info", help="dimensiones, modo, formato, peso")
    s.add_argument("inputs", nargs="+")
    s.set_defaults(func=cmd_info)

    s = sub.add_parser("resize", help="redimensionar (fit cover/contain/stretch)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--width", type=int); s.add_argument("--height", type=int)
    s.add_argument("--pct", type=float, help="escala porcentual")
    s.add_argument("--aspect", help="forzar relacion ej 1:1, 16:9")
    s.add_argument("--fit", choices=["cover", "contain", "stretch"], default="cover")
    s.add_argument("--pad", help="color de relleno si fit=contain (ej white o 255,255,255)")
    s.set_defaults(func=cmd_resize)

    s = sub.add_parser("convert", help="cambiar de formato por extension de salida")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--quality", type=int)
    s.set_defaults(func=cmd_convert)

    s = sub.add_parser("compress", help="bajar peso (--target-kb o --quality)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--target-kb", type=int); s.add_argument("--quality", type=int)
    s.set_defaults(func=cmd_compress)

    s = sub.add_parser("crop", help="recortar (--box x,y,w,h o --aspect W:H centrado)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--box"); s.add_argument("--aspect")
    s.set_defaults(func=cmd_crop)

    s = sub.add_parser("rotate", help="rotar grados (sentido horario)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--deg", type=float, required=True)
    s.add_argument("--expand", action="store_true")
    s.set_defaults(func=cmd_rotate)

    s = sub.add_parser("flip", help="espejar h (horizontal) o v (vertical)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--axis", choices=["h", "v"], default="h")
    s.set_defaults(func=cmd_flip)

    s = sub.add_parser("pad", help="encajar en lienzo WxH con relleno (letterbox)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--size", required=True, help="ej 1080x1080")
    s.add_argument("--color", default="white")
    s.set_defaults(func=cmd_pad)

    s = sub.add_parser("thumb", help="miniatura cuadrada de lado N (mantiene proporcion)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--size", type=int, default=256)
    s.set_defaults(func=cmd_thumb)

    s = sub.add_parser("watermark", help="marca de agua de texto o logo")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--text"); s.add_argument("--logo")
    s.add_argument("--pos", default="br", help="t/m/b + l/c/r, ej br, tl, mc")
    s.add_argument("--opacity", type=int, default=70)
    s.add_argument("--scale", type=int, help="%% del ancho (texto~5, logo~18)")
    s.set_defaults(func=cmd_watermark)

    s = sub.add_parser("grid", help="collage en grilla de varias imagenes")
    s.add_argument("output")
    s.add_argument("--inputs", required=True, help="rutas separadas por coma")
    s.add_argument("--cols", type=int, default=2)
    s.add_argument("--cell", type=int, default=500)
    s.add_argument("--gap", type=int, default=10)
    s.add_argument("--bg", default="white")
    s.set_defaults(func=cmd_grid)

    s = sub.add_parser("palette", help="extraer colores dominantes (hex)")
    s.add_argument("input")
    s.add_argument("--colors", type=int, default=6)
    s.set_defaults(func=cmd_palette)

    s = sub.add_parser("round", help="esquinas redondeadas (PNG con transparencia)")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--radius", type=int, default=40)
    s.set_defaults(func=cmd_round)

    s = sub.add_parser("removebg", help="quitar fondo (requiere rembg)")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(func=cmd_removebg)

    s = sub.add_parser("filter", help="filtro: blur/sharpen/grayscale/contour/smooth/edge")
    s.add_argument("name"); s.add_argument("input"); s.add_argument("output")
    s.add_argument("--amount", type=float)
    s.set_defaults(func=cmd_filter)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)

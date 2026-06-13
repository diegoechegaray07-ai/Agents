#!/usr/bin/env python3
"""Regenera los materiales QR de Pets Company en un solo paso.

Encapsula el flujo completo y sus gotchas:
  - (opcional) regenera el QR oficial interoperable Coelsa desde un CVU/CBU,
  - borra cada salida antes de recrearla (evita el OSError [Errno 22] que tira
    PIL al sobrescribir archivos que OneDrive tiene como placeholder),
  - regenera cartel base PNG, cartel A4 PDF y sticker (PNG + PDF).

Uso:
    python regenerar.py                      # usa el QR oficial actual
    python regenerar.py --cbu <CVU22>        # regenera primero el QR oficial
    python regenerar.py --proyecto <ruta>    # si el proyecto QR está en otro lado
"""

import argparse
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Ruta por defecto del proyecto QR (ajustable con --proyecto).
PROYECTO_DEFAULT = Path(
    r"D:\OneDrive\DCG y ROE - Diego\Diego\Antigravity\QR"
)

# (script, args extra, archivos de salida a borrar antes de regenerar)
PASOS = [
    ("src/qr_petscompany.py", [], ["data/cartel_petscompany.png"]),
    ("src/cartel_a4_pdf.py", [], ["data/cartel_petscompany_A4.pdf"]),
    ("src/sticker_petscompany.py",
     ["--salida", "data/sticker_petscompany.png"], ["data/sticker_petscompany.png"]),
    ("src/sticker_petscompany.py",
     ["--salida", "data/sticker_petscompany.pdf"], ["data/sticker_petscompany.pdf"]),
]


def _correr(proyecto: Path, script: str, args: list[str]) -> None:
    cmd = [sys.executable, script, *args]
    print(f"  $ python {script} {' '.join(args)}".rstrip())
    r = subprocess.run(cmd, cwd=proyecto)
    if r.returncode != 0:
        raise SystemExit(f"Falló: {script} (código {r.returncode})")


def main(argv=None):
    p = argparse.ArgumentParser(description="Regenera los materiales QR de Pets Company")
    p.add_argument("--cbu", help="CVU/CBU de 22 dígitos; si se pasa, regenera el QR oficial primero")
    p.add_argument("--alias", help="Alias (default del script: petscompany)")
    p.add_argument("--cuit", help="CUIT del titular (default del script)")
    p.add_argument("--titular", help="Nombre del titular (default del script)")
    p.add_argument("--proyecto", type=Path, default=PROYECTO_DEFAULT,
                   help="Ruta del proyecto QR")
    args = p.parse_args(argv)

    proyecto = args.proyecto.expanduser().resolve()
    if not (proyecto / "src").is_dir():
        raise SystemExit(f"No encuentro el proyecto QR en: {proyecto}\n"
                         f"Pasá la ruta correcta con --proyecto.")

    # 1) (Opcional) regenerar el QR oficial interoperable desde el CVU.
    if args.cbu:
        print("Regenerando QR oficial interoperable (Coelsa/EMVCo)...")
        extra = ["--cbu", args.cbu]
        for flag, val in (("--alias", args.alias), ("--cuit", args.cuit),
                          ("--titular", args.titular)):
            if val:
                extra += [flag, val]
        (proyecto / "assets" / "qr_oficial.png").unlink(missing_ok=True)
        _correr(proyecto, "src/qr_interoperable.py", extra)
    else:
        oficial = proyecto / "assets" / "qr_oficial.png"
        estado = "presente" if oficial.exists() else "NO existe (se generará desde el alias)"
        print(f"Sin --cbu: uso el QR oficial actual ({estado}).")

    # 2) Regenerar los materiales (borrando cada salida antes, por el lock de OneDrive).
    print("Regenerando materiales...")
    for script, extra, salidas in PASOS:
        for s in salidas:
            (proyecto / s).unlink(missing_ok=True)
        _correr(proyecto, script, extra)

    print("\n✅ Listo. Materiales en:", proyecto / "data")
    for s in ("cartel_petscompany.png", "cartel_petscompany_A4.pdf",
              "sticker_petscompany.png", "sticker_petscompany.pdf"):
        print("   -", s)


if __name__ == "__main__":
    main()

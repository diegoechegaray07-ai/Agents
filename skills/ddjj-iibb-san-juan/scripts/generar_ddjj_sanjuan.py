#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la liquidación de la DDJJ mensual de Ingresos Brutos de San Juan
(régimen local) a partir del Excel de "Mis Comprobantes Emitidos" de ARCA.

Calcula la base imponible (neto gravado del período, neteando notas de crédito),
aplica la alícuota, resta las deducciones indicadas y produce un PDF de
liquidación con el saldo a pagar.
"""

import argparse
import sys
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

# ----------------------------------------------------------------------------
# Paleta (verde — distingue el documento de IIBB del informe azul de ARCA)
# ----------------------------------------------------------------------------
C_BANDA     = colors.HexColor("#059669")  # verde vivo — banda y acentos
C_HEADER_BG = colors.HexColor("#022C22")  # verde muy oscuro — fondo encabezado
C_HEADER_MID= colors.HexColor("#064E3B")  # verde medio — panel derecho
C_ACENTO    = colors.HexColor("#34D399")  # verde claro — KPI secundarios
C_ACENTO2   = colors.HexColor("#A7F3D0")  # verde muy claro — labels
C_TABLE_HDR = colors.HexColor("#064E3B")
C_ALT       = colors.HexColor("#ECFDF5")
C_TOT_BG    = colors.HexColor("#D1FAE5")
C_TOT_LINE  = colors.HexColor("#059669")
C_BOX       = colors.HexColor("#A7F3D0")
C_GRID      = colors.HexColor("#D1FAE5")
C_SEC_BG    = colors.HexColor("#F0FDF4")
C_MUTED     = colors.HexColor("#64748B")
C_CHIP_BG   = colors.HexColor("#022017")

HEADER_H = 50 * mm
ML, MR = 16 * mm, 14 * mm
W, H = A4


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------
def money(v):
    """Formatea 1234.5 -> '$ 1.234,50'."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        v = 0.0
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-$ {s}" if v < 0 else f"$ {s}"


def find_col(df, *candidatos):
    """Busca una columna por coincidencia flexible (ignora mayúsculas/espacios)."""
    norm = {str(c).strip().lower(): c for c in df.columns}
    for cand in candidatos:
        key = cand.strip().lower()
        if key in norm:
            return norm[key]
    # coincidencia parcial
    for cand in candidatos:
        key = cand.strip().lower()
        for k, original in norm.items():
            if key in k:
                return original
    return None


def leer_comprobantes(xlsx_path):
    """Lee el xlsx de ARCA. Devuelve un DataFrame normalizado."""
    # El header de "Mis Comprobantes Emitidos" está en la fila 2 (header=1).
    df = pd.read_excel(xlsx_path, header=1)
    # Si quedó casi vacío, probar sin offset.
    if df.shape[1] < 3 or df.dropna(how="all").shape[0] == 0:
        df = pd.read_excel(xlsx_path)

    c_fecha = find_col(df, "Fecha", "Fecha de Emisión", "Fecha Emisión")
    c_tipo  = find_col(df, "Tipo", "Tipo de Comprobante", "Tipo Comp")
    c_neto  = find_col(df, "Neto Gravado Total", "Neto Gravado", "Imp. Neto Gravado")
    c_nograv= find_col(df, "Neto No Gravado", "Imp. Neto No Gravado")
    c_total = find_col(df, "Imp. Total", "Importe Total", "Total")

    if c_neto is None:
        raise ValueError(
            "No se encontró la columna de Neto Gravado en el xlsx. "
            f"Columnas detectadas: {list(df.columns)}"
        )

    out = pd.DataFrame()
    out["fecha"] = df[c_fecha] if c_fecha else ""
    out["tipo"] = df[c_tipo].astype(str) if c_tipo else ""
    out["neto"] = pd.to_numeric(df[c_neto], errors="coerce").fillna(0.0)
    out["nograv"] = (pd.to_numeric(df[c_nograv], errors="coerce").fillna(0.0)
                     if c_nograv else 0.0)
    out["total"] = (pd.to_numeric(df[c_total], errors="coerce").fillna(0.0)
                    if c_total else 0.0)
    # Quitar filas totalmente vacías / sin importe ni tipo.
    out = out[~((out["neto"] == 0) & (out["total"] == 0) & (out["tipo"].str.strip() == ""))]
    return out


def signo_por_tipo(tipo):
    """Notas de crédito restan; el resto suma."""
    t = str(tipo).lower()
    if "cr" in t and ("dito" in t or "edito" in t):  # crédito / credito
        return -1.0
    return 1.0


def fmt_fecha(v):
    if isinstance(v, (datetime, pd.Timestamp)):
        return v.strftime("%d/%m/%Y")
    return str(v).split(" ")[0]


def periodo_predominante(df):
    """Devuelve 'MM/AAAA' del mes con más comprobantes."""
    fechas = pd.to_datetime(df["fecha"], errors="coerce", dayfirst=True)
    fechas = fechas.dropna()
    if fechas.empty:
        return ""
    per = fechas.dt.to_period("M")
    top = per.value_counts().idxmax()
    return f"{top.month:02d}/{top.year}"


# ----------------------------------------------------------------------------
# Encabezado (canvas)
# ----------------------------------------------------------------------------
def make_header(periodo, contribuyente, cuit, alicuota):
    def draw(canvas, doc):
        canvas.saveState()
        top = H
        # Fondo dividido
        canvas.setFillColor(C_HEADER_BG)
        canvas.rect(0, top - HEADER_H, W / 2, HEADER_H, fill=1, stroke=0)
        canvas.setFillColor(C_HEADER_MID)
        canvas.rect(W / 2, top - HEADER_H, W / 2, HEADER_H, fill=1, stroke=0)
        # Banda lateral y línea inferior
        canvas.setFillColor(C_BANDA)
        canvas.rect(0, top - HEADER_H, 5 * mm, HEADER_H, fill=1, stroke=0)
        canvas.rect(0, top - HEADER_H, W, 1.5 * mm, fill=1, stroke=0)
        # Ícono rombo "IB"
        cx, cy = 15 * mm, top - 15 * mm
        canvas.setFillColor(C_BANDA)
        canvas.saveState()
        canvas.translate(cx, cy)
        canvas.rotate(45)
        canvas.rect(-5 * mm, -5 * mm, 10 * mm, 10 * mm, fill=1, stroke=0)
        canvas.restoreState()
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawCentredString(cx, cy - 3, "IB")
        # Título
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 17)
        canvas.drawString(26 * mm, top - 13 * mm, "DDJJ Ingresos Brutos — San Juan")
        canvas.setFillColor(C_ACENTO2)
        canvas.setFont("Helvetica", 9)
        sub = "Régimen Local"
        if cuit:
            sub += f"  ·  CUIT {cuit}"
        if contribuyente:
            sub += f"  ·  {contribuyente}"
        canvas.drawString(26 * mm, top - 19 * mm, sub)
        # Separador
        canvas.setStrokeColor(C_BANDA)
        canvas.setLineWidth(0.6)
        canvas.line(8 * mm, top - 27 * mm, W - 8 * mm, top - 27 * mm)
        # Chips
        chips = [
            ("PERÍODO", periodo or "—"),
            ("CONTRIBUYENTE", contribuyente or "—"),
            ("ALÍCUOTA", f"{alicuota:.2f}%".replace(".", ",")),
        ]
        chip_w = (W - 16 * mm - 2 * 4 * mm) / 3
        x = 8 * mm
        cy0 = top - HEADER_H + 5 * mm
        for label, value in chips:
            canvas.setFillColor(C_CHIP_BG)
            canvas.rect(x, cy0, chip_w, 13 * mm, fill=1, stroke=0)
            canvas.setFillColor(C_BANDA)
            canvas.rect(x, cy0 + 13 * mm - 1.2 * mm, chip_w, 1.2 * mm, fill=1, stroke=0)
            canvas.setFillColor(C_ACENTO2)
            canvas.setFont("Helvetica-Bold", 6.5)
            canvas.drawString(x + 3 * mm, cy0 + 8.5 * mm, label)
            canvas.setFillColor(colors.white)
            canvas.setFont("Helvetica-Bold", 9)
            txt = value if len(str(value)) <= 26 else str(value)[:24] + "…"
            canvas.drawString(x + 3 * mm, cy0 + 3.2 * mm, txt)
            x += chip_w + 4 * mm
        # Footer
        canvas.setStrokeColor(C_BOX)
        canvas.setLineWidth(0.5)
        canvas.line(ML, 16 * mm, W - MR, 16 * mm)
        canvas.setFillColor(C_MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(ML, 12 * mm,
                          "Generado el " + datetime.now().strftime("%d/%m/%Y %H:%M") +
                          "  ·  Liquidación de apoyo — verificar contra la presentación oficial de la DGR San Juan")
        canvas.drawRightString(W - MR, 12 * mm, f"Página {canvas.getPageNumber()}")
        canvas.restoreState()
    return draw


# ----------------------------------------------------------------------------
# Bloques de contenido
# ----------------------------------------------------------------------------
def sec_title(text):
    st = ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=9.5,
                        textColor=C_TABLE_HDR, leftIndent=9, spaceBefore=2,
                        spaceAfter=2, leading=12)
    p = Paragraph(text, st)
    t = Table([[p]], colWidths=[W - ML - MR])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_SEC_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 4, C_BANDA),
        ("BOX", (0, 0), (-1, -1), 0.5, C_BOX),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def kpi_row(base, alicuota, impuesto, saldo, saldo_a_favor):
    usable = W - ML - MR
    cw = usable / 4
    saldo_label = "SALDO A FAVOR" if saldo_a_favor else "SALDO A PAGAR"
    cells = [
        ("BASE IMPONIBLE", money(base), "#34D399", 11),
        ("ALÍCUOTA", f"{alicuota:.2f}%".replace(".", ","), "#34D399", 11),
        ("IMPUESTO DETERMINADO", money(impuesto), "#34D399", 11),
        (saldo_label, money(abs(saldo)), "#FFFFFF", 14),
    ]
    cards = []
    for label, value, hexcolor, size in cells:
        lab = Paragraph(f'<font color="#A7F3D0" size="6.5"><b>{label}</b></font>',
                        ParagraphStyle("l", leading=9))
        val = Paragraph(f'<font color="{hexcolor}" size="{size}"><b>{value}</b></font>',
                        ParagraphStyle("v", leading=size + 3))
        inner = Table([[lab], [val]], colWidths=[cw - 3 * mm])
        inner.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        cards.append(inner)
    t = Table([cards], colWidths=[cw] * 4)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_HEADER_BG),
        ("LINEABOVE", (0, 0), (-1, 0), 3, C_BANDA),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, C_HEADER_MID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def tabla_style(n_filas, con_total=True):
    s = [
        ("BACKGROUND", (0, 0), (-1, 0), C_TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, 0), 2, C_BANDA),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BOX),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ]
    for i in range(1, n_filas):
        if i % 2 == 0:
            s.append(("BACKGROUND", (0, i), (-1, i), C_ALT))
    if con_total:
        s += [
            ("BACKGROUND", (0, -1), (-1, -1), C_TOT_BG),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, -1), (-1, -1), C_TABLE_HDR),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, C_TOT_LINE),
        ]
    return TableStyle(s)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="DDJJ Ingresos Brutos San Juan (local)")
    ap.add_argument("--xlsx", required=True, help="Ruta al xlsx de ARCA")
    ap.add_argument("--salida", required=True, help="Ruta del PDF de salida")
    ap.add_argument("--periodo", default="", help="Período MM/AAAA (default: inferido)")
    ap.add_argument("--contribuyente", default="", help="Razón social")
    ap.add_argument("--cuit", default="", help="CUIT del contribuyente")
    ap.add_argument("--alicuota", type=float, default=3.0, help="Alícuota %% (default 3.0)")
    ap.add_argument("--base-imponible", type=float, default=None,
                    help="Override de base imponible (saltea lectura del Neto Gravado)")
    ap.add_argument("--retenciones", type=float, default=0.0)
    ap.add_argument("--percepciones", type=float, default=0.0)
    ap.add_argument("--perc-bancarias", type=float, default=0.0)
    ap.add_argument("--saldo-favor-anterior", type=float, default=0.0)
    args = ap.parse_args()

    df = leer_comprobantes(args.xlsx)
    df["signo"] = df["tipo"].apply(signo_por_tipo)
    df["neto_neto"] = df["neto"] * df["signo"]

    if args.base_imponible is not None:
        base = args.base_imponible
    else:
        base = float(df["neto_neto"].sum())

    periodo = args.periodo or periodo_predominante(df)
    alic = args.alicuota
    impuesto = round(base * alic / 100.0, 2)
    deducciones = (args.retenciones + args.percepciones +
                   args.perc_bancarias + args.saldo_favor_anterior)
    saldo = round(impuesto - deducciones, 2)
    saldo_a_favor = saldo < 0

    # ---- Resumen por consola ----
    print("=" * 56)
    print("  LIQUIDACIÓN DDJJ INGRESOS BRUTOS — SAN JUAN (local)")
    print("=" * 56)
    print(f"  Período ............... {periodo or '(sin determinar)'}")
    print(f"  Contribuyente ........ {args.contribuyente or '-'}  {args.cuit}")
    print(f"  Base imponible ....... {money(base)}")
    print(f"  Alícuota ............. {alic:.2f}%")
    print(f"  Impuesto determinado . {money(impuesto)}")
    if deducciones:
        print(f"  (-) Retenciones ...... {money(args.retenciones)}")
        print(f"  (-) Percepciones ..... {money(args.percepciones)}")
        print(f"  (-) Perc. bancarias .. {money(args.perc_bancarias)}")
        print(f"  (-) Saldo a favor ant. {money(args.saldo_favor_anterior)}")
        print(f"  (-) Total deducciones  {money(deducciones)}")
    etiqueta = "SALDO A FAVOR" if saldo_a_favor else "SALDO A PAGAR"
    print(f"  {etiqueta} ......... {money(abs(saldo))}")
    print("=" * 56)

    # ---- PDF ----
    doc = SimpleDocTemplate(
        args.salida, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=HEADER_H + 6 * mm, bottomMargin=22 * mm,
    )
    story = []
    story.append(kpi_row(base, alic, impuesto, saldo, saldo_a_favor))
    story.append(Spacer(1, 8 * mm))

    # Determinación del impuesto
    det = [["Concepto", "Importe"],
           ["Base imponible gravada (neto)", money(base)],
           [f"Alícuota aplicada", f"{alic:.2f}%".replace(".", ",")],
           ["Impuesto determinado", money(impuesto)]]
    t_det = Table(det, colWidths=[(W - ML - MR) * 0.62, (W - ML - MR) * 0.38])
    t_det.setStyle(tabla_style(len(det), con_total=True))
    story.append(KeepTogether([sec_title("Determinación del impuesto"),
                               Spacer(1, 2 * mm), t_det]))
    story.append(Spacer(1, 6 * mm))

    # Deducciones
    if deducciones:
        ded_rows = [["Deducción", "Importe"]]
        for lbl, val in [("Retenciones", args.retenciones),
                         ("Percepciones", args.percepciones),
                         ("Percepciones bancarias / aduaneras", args.perc_bancarias),
                         ("Saldo a favor período anterior", args.saldo_favor_anterior)]:
            if val:
                ded_rows.append([lbl, money(val)])
        ded_rows.append(["Total deducciones", money(deducciones)])
        t_ded = Table(ded_rows, colWidths=[(W - ML - MR) * 0.62, (W - ML - MR) * 0.38])
        t_ded.setStyle(tabla_style(len(ded_rows), con_total=True))
        story.append(KeepTogether([sec_title("Deducciones"),
                                   Spacer(1, 2 * mm), t_ded]))
        story.append(Spacer(1, 6 * mm))

    # Resultado
    etiqueta = "Saldo a favor (período siguiente)" if saldo_a_favor else "Saldo a pagar"
    res = [["Concepto", "Importe"],
           ["Impuesto determinado", money(impuesto)],
           ["Total deducciones", money(deducciones)],
           [etiqueta, money(abs(saldo))]]
    t_res = Table(res, colWidths=[(W - ML - MR) * 0.62, (W - ML - MR) * 0.38])
    t_res.setStyle(tabla_style(len(res), con_total=True))
    story.append(KeepTogether([sec_title("Resultado de la liquidación"),
                               Spacer(1, 2 * mm), t_res]))
    story.append(Spacer(1, 6 * mm))

    # Detalle de ventas por fecha
    df_v = df.copy()
    df_v["fecha_str"] = df_v["fecha"].apply(fmt_fecha)
    por_fecha = df_v.groupby("fecha_str").agg(
        n=("neto_neto", "size"), neto=("neto_neto", "sum")).reset_index()
    # ordenar por fecha real
    por_fecha["orden"] = pd.to_datetime(por_fecha["fecha_str"], errors="coerce", dayfirst=True)
    por_fecha = por_fecha.sort_values("orden")
    det_rows = [["Fecha", "Comprob.", "Neto gravado"]]
    for _, r in por_fecha.iterrows():
        det_rows.append([r["fecha_str"], str(int(r["n"])), money(r["neto"])])
    det_rows.append(["TOTAL", str(int(por_fecha["n"].sum())), money(base)])
    t_v = Table(det_rows, colWidths=[(W - ML - MR) * 0.34, (W - ML - MR) * 0.22,
                                     (W - ML - MR) * 0.44], repeatRows=1)
    st_v = tabla_style(len(det_rows), con_total=True)
    st_v.add("ALIGN", (1, 0), (1, -1), "CENTER")
    t_v.setStyle(st_v)
    story.append(sec_title("Detalle de ventas del período"))
    story.append(Spacer(1, 2 * mm))
    story.append(t_v)

    hdr = make_header(periodo, args.contribuyente, args.cuit, alic)
    doc.build(story, onFirstPage=hdr, onLaterPages=hdr)
    print(f"\nPDF generado: {args.salida}")


if __name__ == "__main__":
    sys.exit(main())

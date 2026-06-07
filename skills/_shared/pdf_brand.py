"""Toolkit compartido para armar PDFs de marca con reportlab.

Concentra el lenguaje visual común a los informes (`arca-informe`,
`ddjj-iibb-san-juan`, `getnet-informe`): paleta, encabezado con banda, tarjetas
KPI, títulos de sección y tablas con fila de total y filas alternas. Cada informe
puede pasar su propio acento de color manteniendo el resto del estilo unificado.

No reemplaza el contenido de cada informe: provee los bloques para componerlo.
"""

from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle

from formatting import format_ars, format_pct  # noqa: F401  (re-export por conveniencia)

# Color de marca Pets Company / DCG.
BRAND_CYAN = "#03B0D6"


@dataclass
class Palette:
    """Paleta de un informe. Cambiá `accent` por informe; el resto queda unificado."""
    accent: str = BRAND_CYAN          # acento principal (banda, líneas, KPIs)
    header_bg: str = "#0F172A"        # fondo oscuro del encabezado
    accent_soft: str = "#93C5FD"      # labels y subtítulos sobre fondo oscuro
    table_header: str = "#1E3A5F"     # fondo de encabezados de tabla
    row_alt: str = "#EFF6FF"          # filas alternas
    total_bg: str = "#DBEAFE"         # fila de total
    box: str = "#BFDBFE"              # borde exterior de tablas
    grid: str = "#DBEAFE"            # grilla interna
    muted: str = "#64748B"            # texto secundario / pie

    def c(self, hexname):
        return colors.HexColor(hexname)


def section_title(text, palette=None):
    """Título de sección como flowable (caja con banda izquierda de acento)."""
    palette = palette or Palette()
    style = ParagraphStyle(
        "sec", fontName="Helvetica-Bold", fontSize=9.5,
        textColor=colors.HexColor(palette.table_header), leading=13,
    )
    t = Table([[Paragraph(text, style)]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F7FF")),
        ("LINEBEFORE", (0, 0), (0, -1), 4, colors.HexColor(palette.accent)),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor(palette.box)),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def kpi_row(kpis, palette=None):
    """Fila de tarjetas KPI. `kpis` = lista de (label, valor) ya formateados.

    Devuelve un flowable (Table) con una tarjeta por KPI, fondo oscuro y línea
    superior de acento.
    """
    palette = palette or Palette()
    label_st = ParagraphStyle(
        "kpil", fontName="Helvetica", fontSize=7,
        textColor=colors.HexColor(palette.accent_soft), leading=9,
    )
    val_st = ParagraphStyle(
        "kpiv", fontName="Helvetica-Bold", fontSize=13,
        textColor=colors.white, leading=16,
    )
    fila_lbl = [Paragraph(str(lbl).upper(), label_st) for lbl, _ in kpis]
    fila_val = [Paragraph(str(val), val_st) for _, val in kpis]
    n = len(kpis)
    ancho = f"{100 / n:.4f}%" if n else "100%"
    t = Table([fila_lbl, fila_val], colWidths=[ancho] * n)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(palette.header_bg)),
        ("LINEABOVE", (0, 0), (-1, 0), 3, colors.HexColor(palette.accent)),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, n):
        estilo.append(("LINEBEFORE", (i, 0), (i, -1), 0.5, colors.HexColor(palette.accent_soft)))
    t.setStyle(TableStyle(estilo))
    return t


def data_table(headers, rows, palette=None, total_row=None, col_widths=None,
               align_right_from=1):
    """Tabla de datos con estilo de marca.

    - `headers`: lista de encabezados.
    - `rows`: lista de filas (cada fila lista de celdas, ya formateadas).
    - `total_row`: fila de total opcional (resaltada al pie).
    - `align_right_from`: índice de columna desde la cual alinear a la derecha
      (los montos suelen ir a la derecha; la primera columna a la izquierda).
    """
    palette = palette or Palette()
    data = [list(headers)] + [list(r) for r in rows]
    if total_row is not None:
        data.append(list(total_row))

    t = Table(data, colWidths=col_widths, repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(palette.table_header)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("LINEBELOW", (0, 0), (-1, 0), 2, colors.HexColor(palette.accent)),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(palette.box)),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor(palette.grid)),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (align_right_from, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    # filas alternas (entre header y total)
    ultima_datos = len(data) - (2 if total_row is not None else 1)
    for i in range(1, ultima_datos + 1):
        if i % 2 == 0:
            estilo.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor(palette.row_alt)))
    if total_row is not None:
        estilo += [
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor(palette.total_bg)),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, -1), (-1, -1), colors.HexColor(palette.table_header)),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, colors.HexColor(palette.accent)),
        ]
    t.setStyle(TableStyle(estilo))
    return t


def draw_header_band(canvas, doc, title, subtitle="", chips=None, palette=None,
                     height=42 * mm):
    """Dibuja el encabezado de marca en el canvas (usar en onFirstPage).

    `chips` = lista de (label, valor) que se muestran como mini-cápsulas.
    """
    palette = palette or Palette()
    w, _ = doc.pagesize
    top = doc.pagesize[1]
    # fondo
    canvas.setFillColor(colors.HexColor(palette.header_bg))
    canvas.rect(0, top - height, w, height, fill=1, stroke=0)
    # banda lateral + línea inferior de acento
    canvas.setFillColor(colors.HexColor(palette.accent))
    canvas.rect(0, top - height, 5 * mm, height, fill=1, stroke=0)
    canvas.rect(0, top - height, w, 1.5 * mm, fill=1, stroke=0)
    # título
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(12 * mm, top - 16 * mm, title)
    if subtitle:
        canvas.setFillColor(colors.HexColor(palette.accent_soft))
        canvas.setFont("Helvetica", 9)
        canvas.drawString(12 * mm, top - 22 * mm, subtitle)
    # chips
    if chips:
        x = 12 * mm
        canvas.setFont("Helvetica", 7)
        for label, valor in chips:
            txt = f"{label}: {valor}"
            ancho = canvas.stringWidth(txt, "Helvetica", 7) + 8
            canvas.setFillColor(colors.HexColor("#0A1628"))
            canvas.rect(x, top - 34 * mm, ancho, 6 * mm, fill=1, stroke=0)
            canvas.setFillColor(colors.white)
            canvas.drawString(x + 4, top - 32 * mm, txt)
            x += ancho + 6

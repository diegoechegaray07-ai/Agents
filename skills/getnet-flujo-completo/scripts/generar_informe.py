import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Paleta ─────────────────────────────────────────────────────────────────
AZUL_OSC    = colors.HexColor('#0D3B6E')   # portada fondo
AZUL_MED    = colors.HexColor('#1B4F8A')   # títulos tabla header
AZUL_ACENTO = colors.HexColor('#4DA3E0')   # acento celeste
AZUL_KPI_BG = colors.HexColor('#EBF4FF')   # fondo KPI
AZUL_SEC_BG = colors.HexColor('#F0F7FF')   # fondo título sección
AZUL_ROW1   = colors.HexColor('#EBF4FF')
AZUL_ROW2   = colors.white
AZUL_TOTAL  = colors.HexColor('#D0E8FB')
GRIS_TEXTO  = colors.HexColor('#444444')
GRIS_LEVE   = colors.HexColor('#AACCEE')


def fmt_ars(val):
    if pd.isna(val): return '$ 0'
    return f'$ {int(round(val)):,}'.replace(',', '.')


# ── Tabla de datos genérica ─────────────────────────────────────────────────
def build_table(header_row, data_rows, col_widths, total_row=None):
    rows = [header_row] + data_rows
    if total_row:
        rows.append(total_row)
    n = len(rows)
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND',    (0,0),  (-1,0),  AZUL_MED),
        ('TEXTCOLOR',     (0,0),  (-1,0),  colors.white),
        ('FONTNAME',      (0,0),  (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),  (-1,0),  8),
        ('ALIGN',         (0,0),  (-1,0),  'CENTER'),
        ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),  (-1,-1), 4),
        ('BOTTOMPADDING', (0,0),  (-1,-1), 4),
        ('LEFTPADDING',   (0,0),  (-1,-1), 5),
        ('RIGHTPADDING',  (0,0),  (-1,-1), 5),
        ('GRID',          (0,0),  (-1,-1), 0.25, GRIS_LEVE),
        ('ROWBACKGROUNDS',(0,1),  (-1, n-2 if total_row else -1),
                          [AZUL_ROW2, AZUL_ROW1]),
        ('LINEBELOW',     (0,0),  (-1,0),  1, AZUL_ACENTO),
    ]
    if total_row:
        idx = n - 1
        style += [
            ('BACKGROUND', (0,idx), (-1,idx), AZUL_TOTAL),
            ('FONTNAME',   (0,idx), (-1,idx), 'Helvetica-Bold'),
            ('LINEABOVE',  (0,idx), (-1,idx), 0.8, AZUL_MED),
        ]
    t.setStyle(TableStyle(style))
    return t


# ── Título de sección con barra lateral ────────────────────────────────────
def sec_title(texto, ancho):
    """Devuelve un KeepTogether con barra celeste + texto sobre fondo suave."""
    barra = Table([['']], colWidths=[0.22*cm], rowHeights=[0.55*cm])
    barra.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), AZUL_ACENTO),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ]))
    st = ParagraphStyle('sts', fontSize=9.5, fontName='Helvetica-Bold',
                         textColor=AZUL_MED, alignment=TA_LEFT)
    txt_cell = Paragraph(texto, st)
    tbl = Table([[barra, txt_cell]],
                colWidths=[0.3*cm, ancho - 0.3*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), AZUL_SEC_BG),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (1,0), (1,-1),  8),
        ('LEFTPADDING',   (0,0), (0,-1),  0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('LINEBELOW',     (0,0), (-1,-1), 0.5, GRIS_LEVE),
    ]))
    return tbl


def h_row(labels, fs=8):
    return [Paragraph(l, ParagraphStyle('hh', fontSize=fs, fontName='Helvetica-Bold',
             textColor=colors.white, alignment=TA_CENTER)) for l in labels]


# ══════════════════════════════════════════════════════════════════════════════
def generar_informe(archivo, propietario, salida):
    df = pd.read_excel(archivo)
    df['Fecha'] = pd.to_datetime(df['Fecha de Operación'], dayfirst=True).dt.date

    monto_bruto = df['Monto Bruto Transacción'].sum()
    monto_neto  = df['Monto Neto Transacción'].sum()
    cant_tx     = len(df)
    ticket_prom = monto_bruto / cant_tx if cant_tx else 0
    ticket_max  = df['Monto Bruto Transacción'].max()
    ticket_min  = df['Monto Bruto Transacción'].min()
    mostrar_neto = (df['Costo Financiero'].sum() > 0 or df['IVA CFT'].sum() > 0)

    fecha_desde = df['Fecha'].min().strftime('%d/%m/%Y')
    fecha_hasta = df['Fecha'].max().strftime('%d/%m/%Y')

    doc = SimpleDocTemplate(
        salida, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.3*cm, bottomMargin=1.3*cm
    )
    ancho = A4[0] - 3.0*cm

    story = []

    # ══════════════════════════════════════════════════════════════════════
    # ENCABEZADO
    # ══════════════════════════════════════════════════════════════════════
    ACENTO = AZUL_ACENTO
    banda_w = 0.55*cm
    texto_w = ancho - banda_w

    st_inf   = ParagraphStyle('inf',  fontSize=7.5, textColor=colors.HexColor('#80B8DC'),
                               fontName='Helvetica', letterSpacing=2)
    st_prop2 = ParagraphStyle('prp',  fontSize=20, textColor=colors.white,
                               fontName='Helvetica-Bold', leading=23)
    st_per2  = ParagraphStyle('prr',  fontSize=8.5, textColor=colors.HexColor('#90BBD9'),
                               fontName='Helvetica')

    contenido = Table([
        [Paragraph('INFORME  DE  VENTAS', st_inf)],
        [Paragraph(propietario, st_prop2)],
        [Spacer(1, 0.06*cm)],
        [Paragraph(f'Período &nbsp;&nbsp; {fecha_desde} — {fecha_hasta}', st_per2)],
    ], colWidths=[texto_w - 1.0*cm])
    contenido.setStyle(TableStyle([
        ('TOPPADDING',    (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ]))

    header_tbl = Table([[Paragraph('', ParagraphStyle('b')), contenido]],
                       colWidths=[banda_w, texto_w])
    header_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), ACENTO),
        ('BACKGROUND', (1,0), (1,-1), AZUL_OSC),
        ('TOPPADDING',    (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING',   (0,0), (0,-1),  0),
        ('RIGHTPADDING',  (0,0), (0,-1),  0),
        ('LEFTPADDING',   (1,0), (1,-1),  18),
        ('RIGHTPADDING',  (1,0), (1,-1),  12),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(KeepTogether([header_tbl]))
    story.append(Spacer(1, 0.3*cm))

    # ══════════════════════════════════════════════════════════════════════
    # KPIs — una sola fila de 5 (o 6 si neto)
    # ══════════════════════════════════════════════════════════════════════
    kpis = [
        ('Monto Bruto',   fmt_ars(monto_bruto), '▲'),
        ('Transacciones', str(cant_tx),          '#'),
        ('Ticket Prom.',  fmt_ars(ticket_prom),  '~'),
        ('Ticket Máx.',   fmt_ars(ticket_max),   '↑'),
        ('Ticket Mín.',   fmt_ars(ticket_min),   '↓'),
    ]
    if mostrar_neto:
        kpis.insert(3, ('Monto Neto', fmt_ars(monto_neto), '='))

    n_kpi = len(kpis)
    kw = ancho / n_kpi

    def kpi_card(label, valor, icono, w):
        # Encabezado coloreado con label
        head = Table([
            [Paragraph(f'<font size="7" color="#FFFFFF">{label.upper()}</font>',
                       ParagraphStyle('kh', fontName='Helvetica-Bold',
                                      alignment=TA_CENTER))]
        ], colWidths=[w - 0.3*cm])
        head.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), AZUL_MED),
            ('TOPPADDING',    (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING',   (0,0), (-1,-1), 2),
            ('RIGHTPADDING',  (0,0), (-1,-1), 2),
        ]))
        # Valor
        body = Table([
            [Paragraph(valor, ParagraphStyle('kv', fontSize=10.5,
                        fontName='Helvetica-Bold', textColor=AZUL_MED,
                        alignment=TA_CENTER))],
        ], colWidths=[w - 0.3*cm])
        body.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), AZUL_KPI_BG),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 2),
            ('RIGHTPADDING',  (0,0), (-1,-1), 2),
            ('LINEBELOW',     (0,0), (-1,-1), 2, AZUL_ACENTO),
            ('BOX',           (0,0), (-1,-1), 0.4, GRIS_LEVE),
        ]))
        card = Table([[head], [body]], colWidths=[w - 0.3*cm])
        card.setStyle(TableStyle([
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        outer = Table([[card]], colWidths=[w])
        outer.setStyle(TableStyle([
            ('LEFTPADDING',   (0,0), (-1,-1), 3),
            ('RIGHTPADDING',  (0,0), (-1,-1), 3),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        return outer

    kpi_row = [kpi_card(k[0], k[1], k[2], kw) for k in kpis]
    kpi_tbl = Table([kpi_row], colWidths=[kw]*n_kpi)
    kpi_tbl.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(KeepTogether([kpi_tbl]))
    story.append(Spacer(1, 0.35*cm))

    # ══════════════════════════════════════════════════════════════════════
    # TABLAS RESUMEN — 3 tablas en la página 1, sin cortes
    # Disposición: [Por Día | Por Marca] en la misma fila, luego Por Tipo
    # ══════════════════════════════════════════════════════════════════════
    st_n = ParagraphStyle('n',  fontSize=8, fontName='Helvetica')
    st_c = ParagraphStyle('c',  fontSize=8, fontName='Helvetica', alignment=TA_CENTER)
    st_r = ParagraphStyle('r',  fontSize=8, fontName='Helvetica', alignment=TA_RIGHT)
    st_bl= ParagraphStyle('bl', fontSize=8, fontName='Helvetica-Bold')
    st_bc= ParagraphStyle('bc', fontSize=8, fontName='Helvetica-Bold', alignment=TA_CENTER)
    st_br= ParagraphStyle('br', fontSize=8, fontName='Helvetica-Bold', alignment=TA_RIGHT)

    gap = 0.4*cm  # separación entre tablas lado a lado
    mitad = (ancho - gap) / 2

    # ── Columnas según mostrar_neto ─────────────────────────────────────
    if mostrar_neto:
        h_dia_lbls  = ['Fecha', 'Tx', 'Bruto', 'Neto']
        cw_dia      = [mitad*0.32, mitad*0.18, mitad*0.25, mitad*0.25]
        h_marc_lbls = ['Marca', 'Tx', 'Bruto', 'Neto']
        cw_marc     = [mitad*0.32, mitad*0.18, mitad*0.25, mitad*0.25]
        h_tipo_lbls = ['Tipo de Tarjeta', 'Tx', 'Monto Bruto', 'Monto Neto']
        cw_tipo     = [ancho*0.34, ancho*0.16, ancho*0.25, ancho*0.25]
    else:
        h_dia_lbls  = ['Fecha', 'Transacciones', 'Monto Bruto']
        cw_dia      = [mitad*0.36, mitad*0.32, mitad*0.32]
        h_marc_lbls = ['Marca', 'Transacciones', 'Monto Bruto']
        cw_marc     = [mitad*0.36, mitad*0.32, mitad*0.32]
        h_tipo_lbls = ['Tipo de Tarjeta', 'Transacciones', 'Monto Bruto']
        cw_tipo     = [ancho*0.40, ancho*0.30, ancho*0.30]

    # ── Por Día ──────────────────────────────────────────────────────────
    por_dia = df.groupby('Fecha').agg(
        Tx=('Monto Bruto Transacción','count'),
        Bruto=('Monto Bruto Transacción','sum'),
        Neto=('Monto Neto Transacción','sum')
    ).reset_index()

    rows_dia = []
    for _, r in por_dia.iterrows():
        row = [Paragraph(r['Fecha'].strftime('%d/%m/%Y'), st_c),
               Paragraph(str(r['Tx']), st_c),
               Paragraph(fmt_ars(r['Bruto']), st_r)]
        if mostrar_neto: row.append(Paragraph(fmt_ars(r['Neto']), st_r))
        rows_dia.append(row)
    tot_dia = [Paragraph('TOTAL', st_bc), Paragraph(str(cant_tx), st_bc),
               Paragraph(fmt_ars(monto_bruto), st_br)]
    if mostrar_neto: tot_dia.append(Paragraph(fmt_ars(monto_neto), st_br))
    tbl_dia = build_table(h_row(h_dia_lbls), rows_dia, cw_dia, tot_dia)

    # ── Por Marca ─────────────────────────────────────────────────────────
    df['Marca_d'] = df.apply(
        lambda r: str(r['Billetera']) if (pd.isna(r['Marca']) or str(r['Marca'])=='nan')
                  else str(r['Marca']).upper(), axis=1)
    df['Marca_d'] = df['Marca_d'].replace('nan', 'QR / Billetera')

    por_marca = df.groupby('Marca_d').agg(
        Tx=('Monto Bruto Transacción','count'),
        Bruto=('Monto Bruto Transacción','sum'),
        Neto=('Monto Neto Transacción','sum')
    ).reset_index().sort_values('Bruto', ascending=False)

    rows_marca = []
    for _, r in por_marca.iterrows():
        row = [Paragraph(str(r['Marca_d']), st_n),
               Paragraph(str(r['Tx']), st_c),
               Paragraph(fmt_ars(r['Bruto']), st_r)]
        if mostrar_neto: row.append(Paragraph(fmt_ars(r['Neto']), st_r))
        rows_marca.append(row)
    tot_marc = [Paragraph('TOTAL', st_bl), Paragraph(str(cant_tx), st_bc),
                Paragraph(fmt_ars(monto_bruto), st_br)]
    if mostrar_neto: tot_marc.append(Paragraph(fmt_ars(monto_neto), st_br))
    tbl_marc = build_table(h_row(h_marc_lbls), rows_marca, cw_marc, tot_marc)

    # ── Por Tipo ──────────────────────────────────────────────────────────
    por_tipo = df.groupby('Tipo', dropna=False).agg(
        Tx=('Monto Bruto Transacción','count'),
        Bruto=('Monto Bruto Transacción','sum'),
        Neto=('Monto Neto Transacción','sum')
    ).reset_index().sort_values('Bruto', ascending=False)

    rows_tipo = []
    for _, r in por_tipo.iterrows():
        tipo_str = str(r['Tipo']) if not pd.isna(r['Tipo']) else '—'
        row = [Paragraph(tipo_str, st_n),
               Paragraph(str(r['Tx']), st_c),
               Paragraph(fmt_ars(r['Bruto']), st_r)]
        if mostrar_neto: row.append(Paragraph(fmt_ars(r['Neto']), st_r))
        rows_tipo.append(row)
    tot_tipo = [Paragraph('TOTAL', st_bl), Paragraph(str(cant_tx), st_bc),
                Paragraph(fmt_ars(monto_bruto), st_br)]
    if mostrar_neto: tot_tipo.append(Paragraph(fmt_ars(monto_neto), st_br))
    tbl_tipo = build_table(h_row(h_tipo_lbls), rows_tipo, cw_tipo, tot_tipo)

    # ── Layout: Día + Marca lado a lado, luego Tipo ───────────────────────
    sec_dia  = sec_title('Ventas por Día', mitad)
    sec_marc = sec_title('Ventas por Marca', mitad)
    sec_tipo = sec_title('Ventas por Tipo de Tarjeta', ancho)

    # Fila izquierda: título + tabla Día
    bloque_dia = Table(
        [[sec_dia], [Spacer(1, 0.1*cm)], [tbl_dia]],
        colWidths=[mitad]
    )
    bloque_dia.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # Fila derecha: título + tabla Marca
    bloque_marc = Table(
        [[sec_marc], [Spacer(1, 0.1*cm)], [tbl_marc]],
        colWidths=[mitad]
    )
    bloque_marc.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # Separador invisible entre columnas
    sep = Table([['']], colWidths=[gap])
    sep.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),
                              ('RIGHTPADDING',(0,0),(-1,-1),0),
                              ('TOPPADDING',(0,0),(-1,-1),0),
                              ('BOTTOMPADDING',(0,0),(-1,-1),0)]))

    fila_dual = Table([[bloque_dia, sep, bloque_marc]],
                      colWidths=[mitad, gap, mitad])
    fila_dual.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    bloque_tipo = Table(
        [[sec_tipo], [Spacer(1, 0.1*cm)], [tbl_tipo]],
        colWidths=[ancho]
    )
    bloque_tipo.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(KeepTogether([fila_dual]))
    story.append(Spacer(1, 0.35*cm))
    story.append(KeepTogether([bloque_tipo]))

    # ══════════════════════════════════════════════════════════════════════
    # DETALLE — siempre en página nueva
    # ══════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(sec_title('Detalle de Transacciones', ancho))
    story.append(Spacer(1, 0.1*cm))

    # ¿Mostrar Plan Cuotas? Solo si al menos una fila tiene contenido
    tiene_cuotas = df['Plan Cuotas'].apply(
        lambda x: not (pd.isna(x) or str(x).strip() in ['', 'nan', '0'])
    ).any()

    # Anchos base por columna
    base_hdrs = ['Fecha de Operación','Billetera','Marca','Tipo','Nro Cupón']
    base_cw   = [2.85*cm, 2.5*cm, 1.6*cm, 2.4*cm, 2.85*cm]

    if tiene_cuotas:
        base_hdrs.append('Plan Cuotas')
        base_cw.append(1.4*cm)

    if mostrar_neto:
        hdrs_det = base_hdrs + ['Monto Bruto', 'Monto Neto']
        fijo = sum(base_cw)
        sobre = (ancho - fijo) / 2
        cw_det = base_cw + [sobre, sobre]
    else:
        hdrs_det = base_hdrs + ['Monto Bruto']
        fijo = sum(base_cw)
        cw_det = base_cw + [ancho - fijo]

    s7  = ParagraphStyle('s7',  fontSize=7.2, fontName='Helvetica')
    s7c = ParagraphStyle('s7c', fontSize=7.2, fontName='Helvetica', alignment=TA_CENTER)
    s7r = ParagraphStyle('s7r', fontSize=7.2, fontName='Helvetica', alignment=TA_RIGHT)
    s7b = ParagraphStyle('s7b', fontSize=7.2, fontName='Helvetica-Bold')
    s7bc= ParagraphStyle('s7bc',fontSize=7.2, fontName='Helvetica-Bold', alignment=TA_CENTER)
    s7br= ParagraphStyle('s7br',fontSize=7.2, fontName='Helvetica-Bold', alignment=TA_RIGHT)

    rows_det = []
    for _, r in df.iterrows():
        marca  = str(r['Marca']).upper() if not pd.isna(r['Marca']) else '—'
        billet = str(r['Billetera']) if not pd.isna(r['Billetera']) else '—'
        cupon  = str(r['Nro de Cupón']) if str(r['Nro de Cupón']) not in ['-','nan',''] else '—'
        cv     = r['Plan Cuotas']
        cuotas = '—' if (pd.isna(cv) if not isinstance(cv, str) else cv in ['nan','']) else str(cv)
        fecha_s= pd.to_datetime(r['Fecha de Operación'], dayfirst=True).strftime('%d/%m/%Y %H:%M')
        row = [Paragraph(fecha_s, s7), Paragraph(billet, s7c), Paragraph(marca, s7c),
               Paragraph(str(r['Tipo']), s7c), Paragraph(cupon, s7c)]
        if tiene_cuotas:
            row.append(Paragraph(cuotas, s7c))
        row.append(Paragraph(fmt_ars(r['Monto Bruto Transacción']), s7r))
        if mostrar_neto:
            row.append(Paragraph(fmt_ars(r['Monto Neto Transacción']), s7r))
        rows_det.append(row)

    tot_det = [Paragraph('TOTAL', s7b), Paragraph('', s7c), Paragraph('', s7c),
               Paragraph('', s7c), Paragraph(f'{cant_tx} op.', s7bc)]
    if tiene_cuotas:
        tot_det.append(Paragraph('', s7c))
    tot_det.append(Paragraph(fmt_ars(monto_bruto), s7br))
    if mostrar_neto:
        tot_det.append(Paragraph(fmt_ars(monto_neto), s7br))

    story.append(build_table(
        h_row(hdrs_det, fs=7.5), rows_det, cw_det, tot_det
    ))

    doc.build(story)
    print(f"Generado: {salida}")


if __name__ == '__main__':
    import sys
    # Uso: python generar_informe.py <archivo.xlsx> <propietario> <salida.pdf>
    if len(sys.argv) != 4:
        print("Uso: python generar_informe.py <archivo.xlsx> <propietario> <salida.pdf>")
        sys.exit(1)
    generar_informe(sys.argv[1], sys.argv[2], sys.argv[3])

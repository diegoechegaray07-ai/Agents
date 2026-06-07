"""Tests del código compartido (skills/_shared)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "_shared"))

from formatting import format_ars, format_pct  # noqa: E402
import alegra_client as ac  # noqa: E402


# --- formatting ---------------------------------------------------------------

@pytest.mark.parametrize("entrada,esperado", [
    (1234.5, "$ 1.234,50"),
    (0, "$ 0,00"),
    (-17690.61, "$ -17.690,61"),
    (1000000, "$ 1.000.000,00"),
    ("no-numero", "$ 0,00"),
])
def test_format_ars(entrada, esperado):
    assert format_ars(entrada) == esperado


def test_format_pct():
    assert format_pct(21) == "21%"
    assert format_pct(21.5, 1) == "21.5%"


# --- alegra_client (sin red) --------------------------------------------------

def test_map_payment_method():
    assert ac.map_payment_method("cash") == "Efectivo"
    assert ac.map_payment_method("transfer") == "Transferencia"
    assert ac.map_payment_method("otro") == "otro"  # passthrough


def test_turno():
    assert ac.turno("2026-05-23 10:15:00") == "Mañana"
    assert ac.turno("2026-05-23 18:40:00") == "Noche"
    assert ac.turno("basura") == "Desconocido"


def _fake_fetcher_factory(paginas):
    """Devuelve un fetcher que sirve páginas según el parámetro start de la URL."""
    def fetcher(url, auth):
        start = int(url.split("start=")[1].split("&")[0])
        idx = start // ac.PAGE_SIZE
        return paginas[idx] if idx < len(paginas) else []
    return fetcher


def test_pagination_dedup_and_filter():
    # Página 0: 30 facturas del 2026-05-23; página 1: 30 más viejas (corte)
    p0 = [{"id": i, "date": "2026-05-23", "total": "100"} for i in range(30)]
    p0[5]["id"] = 4  # duplicado del id 4 -> debe deduplicarse
    p1 = [{"id": 100 + i, "date": "2026-05-20", "total": "50"} for i in range(30)]
    cli = ac.AlegraClient(user="u", token="t", fetcher=_fake_fetcher_factory([p0, p1]))

    dia = cli.invoices_on("2026-05-23")
    ids = [i["id"] for i in dia]
    assert all(i["date"] == "2026-05-23" for i in dia)
    assert len(ids) == len(set(ids))      # sin duplicados
    assert 100 not in ids                 # las viejas quedaron fuera


def test_find_by_formatted_number():
    inv = [
        {"id": 1, "numberTemplate": {"formattedNumber": "00001252"}},
        {"id": 2, "numberTemplate": {"formattedNumber": "00001253"}},
    ]
    assert ac.AlegraClient.find_by_formatted_number(inv, "00001253")["id"] == 2
    assert ac.AlegraClient.find_by_formatted_number(inv, "99999999") is None


def test_load_credentials_from_env(monkeypatch):
    monkeypatch.setenv("ALEGRA_USER", "user@example.com")
    monkeypatch.setenv("ALEGRA_TOKEN", "tok123")
    assert ac.load_credentials() == ("user@example.com", "tok123")


# --- pdf_brand (genera un PDF real) -------------------------------------------

def test_pdf_brand_genera_pdf(tmp_path):
    pytest.importorskip("reportlab")
    import pdf_brand as pb
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Spacer

    salida = tmp_path / "demo.pdf"
    pal = pb.Palette()
    doc = SimpleDocTemplate(str(salida), pagesize=A4, topMargin=46 * 2.83)
    story = [
        pb.kpi_row([("Total", pb.format_ars(123456)), ("Ventas", "42")], pal),
        Spacer(1, 12),
        pb.section_title("Detalle", pal),
        pb.data_table(
            ["Fecha", "Neto", "Total"],
            [["01/05", pb.format_ars(100), pb.format_ars(121)],
             ["02/05", pb.format_ars(200), pb.format_ars(242)]],
            palette=pal,
            total_row=["Total", pb.format_ars(300), pb.format_ars(363)],
        ),
    ]
    doc.build(
        story,
        onFirstPage=lambda c, d: pb.draw_header_band(
            c, d, "Informe demo", "Pets Company", [("PERÍODO", "May 2026")], pal),
    )
    assert salida.exists() and salida.stat().st_size > 1000

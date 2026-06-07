"""Cliente compartido de la API de Alegra (Pets Company).

Centraliza lo que antes estaba sólo documentado en prosa en la skill `alegra-api`:
auth desde `.env`, paginación (la API tope a 30 por request), el workaround de
que el filtro de fechas server-side no es confiable (se filtra en Python),
deduplicación, mapeo de medios de pago y clasificación de turnos.

Credenciales: NUNCA hardcodear. Se leen de las variables de entorno
`ALEGRA_USER` y `ALEGRA_TOKEN` (o de un archivo `.env`). El token va rotado y
fuera del control de versiones.

Uso típico:

    from alegra_client import AlegraClient
    cli = AlegraClient()                      # toma credenciales del entorno/.env
    ventas = cli.invoices_on("2026-05-23")    # facturas de un día
    total = sum(float(i["total"]) for i in ventas)
"""

import base64
import json
import os
import urllib.request

BASE_URL = "https://app.alegra.com/api/v1/"
PAGE_SIZE = 30  # tope de la API por request

PAYMENT_METHODS = {
    "cash": "Efectivo",
    "debit-card": "Débito",
    "transfer": "Transferencia",
    "credit-card": "Crédito",
}


def map_payment_method(code):
    """`cash` -> `Efectivo`, etc. Devuelve el código si no está mapeado."""
    return PAYMENT_METHODS.get(code, code)


def turno(datetime_str):
    """Clasifica una factura por horario: 'Mañana' (<14h) o 'Noche' (>=14h).

    Pets Company abre 9:30-14:00 y 17:30-21:00; el corte en 14 separa los turnos.
    """
    try:
        hora = int(str(datetime_str)[11:13])
    except (TypeError, ValueError, IndexError):
        return "Desconocido"
    return "Mañana" if hora < 14 else "Noche"


def load_credentials():
    """Devuelve (user, token) desde el entorno o un `.env` cercano.

    Busca `ALEGRA_USER`/`ALEGRA_TOKEN` en el entorno; si falta, intenta leer un
    `.env` en el cwd o junto a este archivo. Lanza RuntimeError si no las encuentra.
    """
    user = os.environ.get("ALEGRA_USER")
    token = os.environ.get("ALEGRA_TOKEN")
    if user and token:
        return user, token

    for ruta in (os.path.join(os.getcwd(), ".env"),
                 os.path.join(os.path.dirname(__file__), ".env")):
        if os.path.exists(ruta):
            with open(ruta, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea or linea.startswith("#") or "=" not in linea:
                        continue
                    k, v = linea.split("=", 1)
                    if k.strip() == "ALEGRA_USER" and not user:
                        user = v.strip()
                    elif k.strip() == "ALEGRA_TOKEN" and not token:
                        token = v.strip()
    if not (user and token):
        raise RuntimeError(
            "Faltan credenciales de Alegra. Definí ALEGRA_USER y ALEGRA_TOKEN "
            "en el entorno o en un archivo .env (no las pongas en el código)."
        )
    return user, token


def _default_fetcher(url, auth_header):
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


class AlegraClient:
    """Cliente mínimo de Alegra con paginación y filtrado en Python.

    `fetcher` es inyectable (recibe `(url, auth_header)` y devuelve JSON ya
    parseado) para poder testear sin red.
    """

    def __init__(self, user=None, token=None, fetcher=None, base_url=BASE_URL):
        if user is None or token is None:
            user, token = load_credentials()
        self._auth = "Basic " + base64.b64encode(f"{user}:{token}".encode()).decode()
        self._fetch = fetcher or _default_fetcher
        self.base_url = base_url

    def _page(self, resource, start, extra=""):
        url = f"{self.base_url}{resource}?limit={PAGE_SIZE}&start={start}{extra}"
        return self._fetch(url, self._auth)

    def fetch_all(self, resource, max_pages=50, stop=None):
        """Trae páginas de un recurso hasta agotar o hasta que `stop(item)` sea True.

        `stop` recibe el último item de la página; útil para cortar cuando las
        fechas ya son anteriores al período buscado (las facturas vienen de más
        reciente a más antigua). Deduplica por `id`.
        """
        vistos, salida = set(), []
        for i in range(max_pages):
            pagina = self._page(resource, i * PAGE_SIZE)
            if not isinstance(pagina, list) or not pagina:
                break
            for item in pagina:
                iid = item.get("id")
                if iid in vistos:
                    continue
                vistos.add(iid)
                salida.append(item)
            if len(pagina) < PAGE_SIZE:
                break
            if stop and stop(pagina[-1]):
                break
        return salida

    def invoices_between(self, date_start, date_end, max_pages=50):
        """Facturas con `date` en [date_start, date_end] (YYYY-MM-DD), filtradas
        en Python porque el filtro server-side de Alegra no es confiable."""
        def stop(ultima):
            return str(ultima.get("date", "")) < date_start
        todas = self.fetch_all("invoices", max_pages=max_pages, stop=stop)
        return [i for i in todas if date_start <= str(i.get("date", "")) <= date_end]

    def invoices_on(self, date, max_pages=50):
        """Facturas de un único día (YYYY-MM-DD)."""
        return self.invoices_between(date, date, max_pages=max_pages)

    @staticmethod
    def find_by_formatted_number(invoices, formatted_number):
        """Busca una factura por `numberTemplate.formattedNumber` (ej. '00001252')."""
        for i in invoices:
            if (i.get("numberTemplate") or {}).get("formattedNumber") == formatted_number:
                return i
        return None

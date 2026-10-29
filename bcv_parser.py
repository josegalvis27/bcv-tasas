import logging
import re
from dataclasses import dataclass, field
from datetime import date, datetime

import requests
import urllib3
import xlrd
from bs4 import BeautifulSoup

import config
from currency_map import BCV_TO_SAP

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


@dataclass
class CurrencyRate:
    bcv_code: str
    country: str
    bid_me_usd: float
    ask_me_usd: float
    bid_bs: float
    ask_bs: float


@dataclass
class BcvRateData:
    fecha_operacion: date
    fecha_valor: date
    currencies: list[CurrencyRate] = field(default_factory=list)


def discover_xls_url() -> str:
    """Scrapea la página del BCV para encontrar el XLS más reciente."""
    url = config.BCV_BASE_URL + config.BCV_STATS_PATH
    logger.info(f"Buscando XLS en {url}")
    resp = requests.get(url, verify=False, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if ".xls" in href and "EstadisticasGeneral" in href:
            if href.startswith("/"):
                href = config.BCV_BASE_URL + href
            logger.info(f"XLS encontrado: {href}")
            return href

    raise RuntimeError("No se encontró ningún archivo XLS en la página del BCV")


def download_xls(url: str) -> bytes:
    """Descarga el archivo XLS."""
    logger.info(f"Descargando {url}")
    resp = requests.get(url, verify=False, timeout=60)
    resp.raise_for_status()
    logger.info(f"Descargado: {len(resp.content)} bytes")
    return resp.content


def _parse_date(text: str) -> date:
    """Extrae una fecha de un string como 'Fecha Operacion: 31/03/2026'."""
    match = re.search(r"(\d{2}/\d{2}/\d{4})", str(text))
    if not match:
        raise ValueError(f"No se pudo extraer fecha de: '{text}'")
    return datetime.strptime(match.group(1), "%d/%m/%Y").date()


def _safe_float(val) -> float:
    """Convierte un valor a float, retorna 0.0 si no es numérico."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def parse_xls(data: bytes) -> BcvRateData:
    """Parsea el XLS del BCV y extrae fechas y tasas de cambio."""
    wb = xlrd.open_workbook(file_contents=data)
    sheet = wb.sheet_by_index(0)

    # Buscar fila con fechas (contiene "Fecha")
    fecha_op = None
    fecha_val = None
    data_start_row = None

    for row_idx in range(min(10, sheet.nrows)):
        row_vals = [sheet.cell_value(row_idx, c) for c in range(sheet.ncols)]
        row_text = " ".join(str(v) for v in row_vals)
        if "Fecha" in row_text and "Operacion" in row_text:
            for val in row_vals:
                s = str(val)
                if "Operacion" in s or "Operación" in s:
                    fecha_op = _parse_date(s)
                if "Valor" in s:
                    fecha_val = _parse_date(s)

    if not fecha_op or not fecha_val:
        raise ValueError("No se encontraron las fechas en el XLS del BCV")

    logger.info(f"Fecha Operación: {fecha_op}, Fecha Valor: {fecha_val}")

    # Buscar fila de encabezado (contiene "Compra" y "Venta")
    for row_idx in range(sheet.nrows):
        row_vals = [str(sheet.cell_value(row_idx, c)) for c in range(sheet.ncols)]
        row_text = " ".join(row_vals)
        if "Compra" in row_text and "Venta" in row_text and "BID" in row_text:
            data_start_row = row_idx + 2  # saltar encabezado + fila vacía
            break

    if data_start_row is None:
        raise ValueError("No se encontró la fila de encabezados en el XLS")

    # Extraer solo las monedas configuradas en currency_map
    target_codes = set(BCV_TO_SAP.keys())
    currencies = []
    for row_idx in range(data_start_row, sheet.nrows):
        code = str(sheet.cell_value(row_idx, 1)).strip()
        if not code or code == "nan" or len(code) != 3:
            if currencies:
                break
            continue

        if code not in target_codes:
            continue

        country = str(sheet.cell_value(row_idx, 2)).strip()
        bid_me_usd = _safe_float(sheet.cell_value(row_idx, 3))
        ask_me_usd = _safe_float(sheet.cell_value(row_idx, 4))
        bid_bs = _safe_float(sheet.cell_value(row_idx, 5))
        ask_bs = _safe_float(sheet.cell_value(row_idx, 6))

        currencies.append(CurrencyRate(
            bcv_code=code,
            country=country,
            bid_me_usd=bid_me_usd,
            ask_me_usd=ask_me_usd,
            bid_bs=bid_bs,
            ask_bs=ask_bs,
        ))
        logger.debug(f"  {code} ({country}): Bs {ask_bs}")

    logger.info(f"Se encontraron {len(currencies)} monedas")
    return BcvRateData(
        fecha_operacion=fecha_op,
        fecha_valor=fecha_val,
        currencies=currencies,
    )


def should_update(fecha_valor: date) -> bool:
    """Retorna True si la fecha valor es futura (hay tasa nueva)."""
    today = date.today()
    if fecha_valor > today:
        logger.info(
            f"Tasa nueva detectada: Fecha Valor {fecha_valor} > Hoy {today}"
        )
        return True
    logger.info(
        f"No hay tasa nueva: Fecha Valor {fecha_valor} <= Hoy {today}"
    )
    return False

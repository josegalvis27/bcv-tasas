import csv
import os
import logging

from bcv_parser import BcvRateData
from currency_map import get_sap_code

logger = logging.getLogger(__name__)


def print_rate_table(data: BcvRateData):
    """Muestra las tasas en una tabla formateada en consola."""
    print()
    print("=" * 80)
    print(f"  TIPO DE CAMBIO DE REFERENCIA - BCV")
    print(f"  Fecha Operación: {data.fecha_operacion.strftime('%d/%m/%Y')}")
    print(f"  Fecha Valor:     {data.fecha_valor.strftime('%d/%m/%Y')}")
    print("=" * 80)
    print()

    header = (
        f"{'BCV':>4} {'SAP':>4} {'País':<22} "
        f"{'Bs/ME Compra':>14} {'Bs/ME Venta':>14} "
        f"{'ME/USD Compra':>14} {'ME/USD Venta':>14}"
    )
    print(header)
    print("-" * len(header))

    for rate in data.currencies:
        sap_code = get_sap_code(rate.bcv_code) or "???"
        print(
            f"{rate.bcv_code:>4} {sap_code:>4} {rate.country:<22} "
            f"{rate.bid_bs:>14.6f} {rate.ask_bs:>14.6f} "
            f"{rate.bid_me_usd:>14.6f} {rate.ask_me_usd:>14.6f}"
        )

    print()


def export_csv(data: BcvRateData, output_dir: str) -> str:
    """Exporta las tasas a un archivo CSV."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"tasas_bcv_{data.fecha_valor.strftime('%Y-%m-%d')}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "bcv_code", "sap_code", "pais",
            "fecha_valor", "bs_me_compra", "bs_me_venta",
            "me_usd_compra", "me_usd_venta",
        ])
        for rate in data.currencies:
            sap_code = get_sap_code(rate.bcv_code) or ""
            writer.writerow([
                rate.bcv_code, sap_code, rate.country,
                data.fecha_valor.strftime("%Y-%m-%d"),
                rate.bid_bs, rate.ask_bs,
                rate.bid_me_usd, rate.ask_me_usd,
            ])

    logger.info(f"CSV exportado: {filepath}")
    print(f"CSV exportado: {filepath}")
    return filepath

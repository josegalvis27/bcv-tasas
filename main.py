#!/usr/bin/env python3
"""
Automatización de tasas de cambio BCV → SAP Business One.
Descarga el tipo de cambio de referencia del BCV y lo reporta o envía a SAP B1.
"""
import argparse
import logging
import os
import sys
from datetime import date

import config
from bcv_parser import discover_xls_url, download_xls, parse_xls, should_update
from output_formatter import print_rate_table, export_csv


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else getattr(logging, config.LOG_LEVEL, logging.INFO)
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/bcv_tasas_{date.today().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    parser = argparse.ArgumentParser(
        description="Tasas de cambio BCV → SAP Business One"
    )
    parser.add_argument(
        "--mode", choices=["report", "push"], default="report",
        help="Modo: report (solo mostrar) o push (enviar a SAP B1)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Ejecutar aunque la fecha valor no sea futura"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostrar qué se enviaría sin llamar a SAP"
    )
    parser.add_argument(
        "--csv", action="store_true",
        help="Exportar tasas a archivo CSV"
    )
    parser.add_argument(
        "--xls-url",
        help="URL directa del XLS (saltar scraping de la página BCV)"
    )
    parser.add_argument(
        "--rate-column", choices=["compra", "venta"], default="venta",
        help="Columna de tasa a usar: compra (BID) o venta (ASK). Default: venta"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Activar logs detallados"
    )

    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # 1. Obtener URL del XLS
        if args.xls_url:
            xls_url = args.xls_url
        else:
            xls_url = discover_xls_url()

        # 2. Descargar y parsear
        xls_data = download_xls(xls_url)
        bcv_data = parse_xls(xls_data)

        # 3. Verificar si hay tasa nueva
        is_new = should_update(bcv_data.fecha_valor)

        if not is_new and not args.force:
            print(
                f"\nNo hay tasa nueva. "
                f"Fecha Valor ({bcv_data.fecha_valor.strftime('%d/%m/%Y')}) "
                f"no es posterior a hoy ({date.today().strftime('%d/%m/%Y')})."
            )
            print("Usa --force para ejecutar de todas formas.")
            # Aún mostramos la tabla en modo report
            if args.mode == "report":
                print_rate_table(bcv_data)
                if args.csv:
                    export_csv(bcv_data, config.OUTPUT_CSV_PATH)
            return 0

        # 4. Modo report
        print_rate_table(bcv_data)
        if args.csv:
            export_csv(bcv_data, config.OUTPUT_CSV_PATH)

        # 5. Modo push
        if args.mode == "push":
            if args.dry_run:
                print("\n[DRY RUN] Se enviarían las siguientes tasas a SAP B1:\n")
                from currency_map import get_sap_code
                for rate in bcv_data.currencies:
                    sap_code = get_sap_code(rate.bcv_code) or "???"
                    value = rate.ask_bs if args.rate_column == "venta" else rate.bid_bs
                    print(f"  {sap_code}: {value} Bs ({args.rate_column})")
                print(f"\nFecha: {bcv_data.fecha_valor.strftime('%Y-%m-%d')}")
                print("[DRY RUN] No se realizaron cambios en SAP.")
                return 0

            config.validate_sap_config()

            from sap_client import SapServiceLayerClient
            with SapServiceLayerClient(
                config.SAP_SERVICE_LAYER_URL,
                config.SAP_COMPANY_DB,
                config.SAP_USERNAME,
                config.SAP_PASSWORD,
            ) as sap:
                results = sap.push_all_rates(
                    bcv_data.currencies,
                    bcv_data.fecha_valor,
                    args.rate_column,
                )

            print(f"\n{'='*40}")
            print(f"  Resultado push SAP B1")
            print(f"{'='*40}")
            print(f"  Exitosas:  {len(results['ok'])}")
            print(f"  Errores:   {len(results['error'])}")
            print(f"  Omitidas:  {len(results['skipped'])}")
            if results["error"]:
                print(f"  Fallaron:  {', '.join(results['error'])}")
            print()

            if results["error"]:
                return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

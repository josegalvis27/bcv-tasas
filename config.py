import os
from dotenv import load_dotenv

load_dotenv()

BCV_BASE_URL = "https://www.bcv.org.ve"
BCV_STATS_PATH = "/estadisticas/tipo-cambio-de-referencia-smc"

SAP_SERVICE_LAYER_URL = os.getenv("SAP_SERVICE_LAYER_URL", "")
SAP_COMPANY_DB = os.getenv("SAP_COMPANY_DB", "")
SAP_USERNAME = os.getenv("SAP_USERNAME", "")
SAP_PASSWORD = os.getenv("SAP_PASSWORD", "")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OUTPUT_CSV_PATH = os.getenv("OUTPUT_CSV_PATH", "./output")


def validate_sap_config():
    missing = []
    if not SAP_SERVICE_LAYER_URL:
        missing.append("SAP_SERVICE_LAYER_URL")
    if not SAP_COMPANY_DB:
        missing.append("SAP_COMPANY_DB")
    if not SAP_USERNAME:
        missing.append("SAP_USERNAME")
    if not SAP_PASSWORD:
        missing.append("SAP_PASSWORD")
    if missing:
        raise ValueError(
            f"Faltan variables de entorno para SAP: {', '.join(missing)}. "
            "Copia .env.example a .env y completa los valores."
        )

import logging

logger = logging.getLogger(__name__)

# Mapeo de códigos de moneda BCV → SAP Business One (ISO 4217)
# Solo las monedas requeridas: USD, EUR, COP
BCV_TO_SAP = {
    "EUR": "EUR",
    "USD": "USD",
    "COP": "COP",
}


def get_sap_code(bcv_code: str) -> str | None:
    sap_code = BCV_TO_SAP.get(bcv_code)
    if sap_code is None:
        logger.warning(f"Código BCV '{bcv_code}' no tiene mapeo a SAP")
    return sap_code

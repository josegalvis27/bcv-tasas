import logging
from datetime import date

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class SapServiceLayerClient:
    def __init__(self, base_url: str, company_db: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.company_db = company_db
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False

    def login(self):
        url = f"{self.base_url}/Login"
        payload = {
            "CompanyDB": self.company_db,
            "UserName": self.username,
            "Password": self.password,
        }
        logger.info(f"Conectando a SAP B1: {self.base_url}")
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        logger.info("Login exitoso en SAP B1")

    def logout(self):
        try:
            url = f"{self.base_url}/Logout"
            self.session.post(url)
            logger.info("Logout de SAP B1")
        except Exception as e:
            logger.warning(f"Error al cerrar sesión SAP: {e}")

    def set_currency_rate(self, currency_code: str, rate_date: date, rate: float) -> bool:
        url = f"{self.base_url}/SBOBobService_SetCurrencyRate"
        payload = {
            "CurrencyCode": currency_code,
            "Date": rate_date.strftime("%Y-%m-%d"),
            "Rate": rate,
        }
        try:
            resp = self.session.post(url, json=payload)
            if resp.status_code == 401:
                logger.warning("Sesión expirada, re-autenticando...")
                self.login()
                resp = self.session.post(url, json=payload)
            resp.raise_for_status()
            logger.info(f"  OK: {currency_code} = {rate} ({rate_date})")
            return True
        except requests.RequestException as e:
            logger.error(f"  ERROR: {currency_code} - {e}")
            return False

    def push_all_rates(self, rates: list, rate_date: date, rate_column: str = "venta") -> dict:
        from currency_map import get_sap_code

        results = {"ok": [], "error": [], "skipped": []}

        for rate in rates:
            sap_code = get_sap_code(rate.bcv_code)
            if not sap_code:
                results["skipped"].append(rate.bcv_code)
                continue

            value = rate.ask_bs if rate_column == "venta" else rate.bid_bs

            if self.set_currency_rate(sap_code, rate_date, value):
                results["ok"].append(sap_code)
            else:
                results["error"].append(sap_code)

        return results

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()

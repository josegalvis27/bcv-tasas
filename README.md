# bcv-tasas

**Automatización de tasas de cambio BCV → SAP Business One.** Descarga las tasas de referencia publicadas por el Banco Central de Venezuela, detecta si hay una publicación nueva y las registra en SAP Business One a través del Service Layer. Lo que antes era un proceso manual diario ahora toma menos de 10 segundos.

*Automates daily Venezuelan Central Bank (BCV) exchange rates into SAP Business One via the Service Layer API.*

## Cómo funciona

1. `bcv_parser.py` descarga y lee el archivo de tasas del BCV (USD, EUR, COP…)
2. `currency_map.py` traduce las monedas a los códigos de SAP
3. `sap_client.py` inicia sesión en el Service Layer y registra las tasas del día
4. `output_formatter.py` / `generar_pdf.py` dejan un respaldo en CSV y un reporte en PDF

## Uso

```bash
pip install -r requirements.txt
cp .env.example .env   # URL del Service Layer, base de datos, usuario y clave
python main.py
```

Python · requests · SAP Business One Service Layer

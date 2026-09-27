# Orderrapportering – refaktorerad version

Detta projekt är en refaktorering av ett befintligt Pythonprogram för orderrapportering. Programmet läser orderdata från en CSV-fil, validerar och bearbetar datan och skapar fyra CSV-rapporter.

Refaktoreringen fokuserar på tydligare ansvar, moduler, logging, felhantering, testbarhet och återanvändbar kod. Beräkningarna från originalprogrammet har behållits.

## Krav

- Python 3.10 eller senare
- pandas
- pytest

Installera beroenden från projektets rotmapp:


pip install -r requirements.txt


## Data

Lägg filen `orders.csv` i mappen:

data/orders.csv


CSV-filen ska innehålla följande obligatoriska kolumner:


order_id
order_date
customer_id
region
product_category
quantity
unit_price
discount
returned


## Köra programmet

Kör från projektets rotmapp:

```bash
python main.py
```

Rapporterna sparas automatiskt i `output/`:

- `overview.csv`
- `sales_by_category.csv`
- `sales_by_region.csv`
- `returns_by_category.csv`

## Köra tester


pytest

Testerna kontrollerar bland annat ordervärden, rabatter, normalisering, sammanställningar och relevanta felscenarier.

## Projektstruktur

```text
order_report_refactored/
├── main.py
├── requirements.txt
├── pytest.ini
├── README.md
├── code_review.md
├── data/
│   └── orders.csv
├── output/
├── order_report/
│   ├── __init__.py
│   ├── config.py
│   ├── data_io.py
│   ├── logging_config.py
│   ├── processing.py
│   ├── reports.py
│   └── validation.py
└── tests/
    ├── conftest.py
    ├── test_processing.py
    ├── test_reports.py
    └── test_validation.py
```

### Modulernas ansvar

- `main.py` – programmets startpunkt och övergripande körflöde.
- `config.py` – innehåller `ReportConfig`, en dataclass för sökvägar.
- `data_io.py` – läser CSV och sparar rapportfiler.
- `validation.py` – kontrollerar obligatoriska kolumner, tom data och varnar för misstänkta värden.
- `processing.py` – tvättar data och beräknar `order_value` och `discounted_value`.
- `reports.py` – skapar översikt, försäljning per kategori/region och returrapport.
- `logging_config.py` – central konfiguration av logging.
- `tests/` – automatiska tester med pytest.
# OrderReportElias

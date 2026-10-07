# pandas-sales-analysis

Data analysis mini project with **pandas**: generate a 50,000-order sales dataset, clean it, compute KPIs and produce a Markdown report.

## What it does

1. `generate_data.py` creates a reproducible synthetic dataset (orders, regions, products, categories, prices).
2. `analysis.py` cleans the data (duplicates, invalid quantities and prices) and computes:
   - global KPIs: orders, revenue, average order value, units
   - revenue and share by region, category and product
   - monthly revenue with month-over-month growth
   - a region x category pivot table
3. `report.py` prints everything and writes `reports/summary.md`.

An example report is committed in [`reports/summary.md`](reports/summary.md).

## Stack

Python 3.11+ · pandas · NumPy · pytest

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m src.generate_data --rows 50000   # creates data/sales.csv
python -m src.report data/sales.csv        # prints and saves the report
pytest
```

## Notes

The data is synthetic. Group-by aggregations use named aggregation, and the tests check that cleaning removes injected dirty rows and that the shares add up to 100%.

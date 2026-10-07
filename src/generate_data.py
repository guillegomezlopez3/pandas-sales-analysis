"""Generate a reproducible synthetic sales dataset.

Usage: python -m src.generate_data --rows 50000
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PRODUCTS = {
    "Laptop": (899.0, "Electronics"), "Phone": (599.0, "Electronics"), "Headphones": (89.0, "Electronics"),
    "Desk": (249.0, "Furniture"), "Chair": (159.0, "Furniture"), "Notebook": (4.5, "Stationery"),
    "Pen pack": (6.0, "Stationery"), "Backpack": (45.0, "Accessories"),
}
REGIONS = ["North", "South", "East", "West"]


def generate(rows: int, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    names = rng.choice(list(PRODUCTS), size=rows)
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, size=rows), unit="D")
    base = np.array([PRODUCTS[n][0] for n in names])
    return pd.DataFrame({
        "order_id": np.arange(1, rows + 1),
        "date": dates,
        "region": rng.choice(REGIONS, size=rows, p=[0.3, 0.25, 0.25, 0.2]),
        "product": names,
        "category": [PRODUCTS[n][1] for n in names],
        "quantity": rng.integers(1, 6, size=rows),
        "unit_price": np.round(base * rng.uniform(0.9, 1.1, size=rows), 2),
    })


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=50_000)
    p.add_argument("--out", default="data/sales.csv")
    a = p.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    generate(a.rows).to_csv(out, index=False)
    print(f"Wrote {a.rows} rows to {out}")


if __name__ == "__main__":
    main()

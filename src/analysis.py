"""Sales analysis with pandas: cleaning, KPIs, monthly trend and top products."""
from pathlib import Path

import pandas as pd


def load_clean(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.drop_duplicates(subset="order_id")
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M")
    return df


def kpis(df: pd.DataFrame) -> dict:
    return {
        "orders": int(len(df)),
        "revenue": round(float(df["revenue"].sum()), 2),
        "avg_order_value": round(float(df["revenue"].mean()), 2),
        "units": int(df["quantity"].sum()),
    }


def revenue_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    out = df.groupby(column).agg(orders=("order_id", "count"), revenue=("revenue", "sum")).round(2)
    out["share_pct"] = (out["revenue"] / out["revenue"].sum() * 100).round(1)
    return out.sort_values("revenue", ascending=False)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    m = df.groupby("month")["revenue"].sum().round(2).to_frame()
    m["mom_growth_pct"] = (m["revenue"].pct_change() * 100).round(1)
    return m


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return revenue_by(df, "product").head(n)


def region_category_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="region", columns="category", values="revenue", aggfunc="sum").round(0)

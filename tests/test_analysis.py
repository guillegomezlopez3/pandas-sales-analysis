import pandas as pd
import pytest

from src import analysis as a
from src.generate_data import generate


@pytest.fixture
def csv_path(tmp_path):
    df = generate(500, seed=1)
    # inject dirty rows: a duplicate id and an invalid quantity
    dirty = pd.concat([df, df.iloc[[0]], df.iloc[[1]].assign(order_id=10_001, quantity=0)])
    p = tmp_path / "sales.csv"
    dirty.to_csv(p, index=False)
    return p


def test_cleaning_removes_duplicates_and_invalid_rows(csv_path):
    df = a.load_clean(csv_path)
    assert len(df) == 500
    assert (df["quantity"] > 0).all()


def test_kpis_are_consistent(csv_path):
    df = a.load_clean(csv_path)
    k = a.kpis(df)
    assert k["orders"] == 500
    assert k["revenue"] == pytest.approx(df["revenue"].sum(), abs=0.01)


def test_shares_add_up_to_100(csv_path):
    df = a.load_clean(csv_path)
    assert a.revenue_by(df, "region")["share_pct"].sum() == pytest.approx(100, abs=0.5)


def test_top_products_sorted(csv_path):
    top = a.top_products(a.load_clean(csv_path), 3)
    assert len(top) == 3
    assert top["revenue"].is_monotonic_decreasing


def test_generator_is_reproducible():
    assert generate(100, seed=5).equals(generate(100, seed=5))

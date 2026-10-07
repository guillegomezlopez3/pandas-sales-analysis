"""Print the analysis and write a Markdown report to reports/summary.md.

Usage: python -m src.report data/sales.csv
"""
import sys
from pathlib import Path

from . import analysis as a


def build_report(path: str) -> str:
    df = a.load_clean(path)
    k = a.kpis(df)
    parts = [
        "# Sales report",
        f"- Orders: {k['orders']:,}\n- Revenue: {k['revenue']:,.2f}\n"
        f"- Average order value: {k['avg_order_value']:,.2f}\n- Units sold: {k['units']:,}",
        "## Revenue by region", a.revenue_by(df, "region").to_markdown(floatfmt=",.2f"),
        "## Revenue by category", a.revenue_by(df, "category").to_markdown(floatfmt=",.2f"),
        "## Top 5 products", a.top_products(df).to_markdown(floatfmt=",.2f"),
        "## Monthly trend", a.monthly_trend(df).to_markdown(floatfmt=",.2f"),
    ]
    return "\n\n".join(parts) + "\n"


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sales.csv"
    text = build_report(path)
    out = Path("reports/summary.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()

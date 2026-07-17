
"""
statistics.py
Statistical summaries for RecoMart EDA.
"""

from pathlib import Path
import pandas as pd


def generate_summary(products, reviews, users, sessions, clickstream, report_dir: Path):
    """Generate markdown summary of processed datasets."""

    datasets = {
        "Products": products,
        "Reviews": reviews,
        "Users": users,
        "Sessions": sessions,
        "Clickstream": clickstream,
    }

    report = ["# Exploratory Data Analysis Summary\n"]

    for name, df in datasets.items():
        report.append(f"## {name}")
        report.append(f"- Rows: {len(df)}")
        report.append(f"- Columns: {len(df.columns)}")
        report.append(f"- Missing Values: {int(df.isnull().sum().sum())}")
        report.append(f"- Duplicate Rows: {int(df.duplicated().sum())}")

        numeric = df.select_dtypes(include="number")
        if not numeric.empty:
            report.append("\n### Numerical Summary")
            report.append(numeric.describe().round(2).to_markdown())

        report.append("\n")

    output = report_dir / "eda_summary.md"
    output.write_text("\n".join(report), encoding="utf-8")


def calculate_sparsity(reviews, report_dir: Path):
    """Calculate user-item interaction sparsity."""

    users = reviews["user_id"].nunique()
    products = reviews["product_id"].nunique()
    interactions = len(reviews)

    possible = users * products

    sparsity = 0.0
    if possible > 0:
        sparsity = 1 - (interactions / possible)

    df = pd.DataFrame({
        "Metric": [
            "Unique Users",
            "Unique Products",
            "Interactions",
            "Possible Interactions",
            "Sparsity"
        ],
        "Value": [
            users,
            products,
            interactions,
            possible,
            round(sparsity, 4)
        ]
    })

    df.to_csv(report_dir / "interaction_statistics.csv", index=False)

    with open(report_dir / "eda_summary.md", "a", encoding="utf-8") as f:
        f.write("\n## Interaction Statistics\n")
        f.write(df.to_markdown(index=False))
        f.write("\n")

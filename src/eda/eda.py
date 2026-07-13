"""
Basic Exploratory Data Analysis
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ---------- Products ----------

products = pd.read_csv(PROCESSED_DIR / "products.csv")

if "category" in products.columns:
    plt.figure(figsize=(10, 5))
    products["category"].value_counts().plot(kind="bar")
    plt.title("Product Category Distribution")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "product_categories.png")
    plt.close()


# ---------- Reviews ----------

reviews = pd.read_csv(PROCESSED_DIR / "reviews.csv")

rating_column = None

for col in ["rating", "ratings"]:
    if col in reviews.columns:
        rating_column = col
        break

if rating_column:
    plt.figure(figsize=(6, 4))
    reviews[rating_column].hist(bins=5)
    plt.title("Rating Distribution")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "ratings_distribution.png")
    plt.close()


# ---------- Top Products ----------

product_column = None

for col in ["product_id", "asin"]:
    if col in reviews.columns:
        product_column = col
        break

if product_column:
    top_products = (
        reviews[product_column]
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(10, 5))
    top_products.plot(kind="bar")
    plt.title("Top 10 Popular Products")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "top_products.png")
    plt.close()


print("EDA completed.")
print(f"Reports saved to: {REPORT_DIR}")

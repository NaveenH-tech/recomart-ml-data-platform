"""
Popularity Based Recommendation
"""

from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")


def get_top_products(top_n=10):

    reviews = pd.read_csv(PROCESSED_DIR / "reviews.csv")

    popularity = (
        reviews.groupby("product_id")
        .agg(
            average_rating=("rating", "mean"),
            review_count=("rating", "count")
        )
        .reset_index()
    )

    popularity = popularity.sort_values(
        ["average_rating", "review_count"],
        ascending=False
    )

    return popularity.head(top_n)


if __name__ == "__main__":

    recommendations = get_top_products(10)

    print(recommendations)

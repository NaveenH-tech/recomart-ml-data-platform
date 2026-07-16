"""
Generate features for recommendation models.
"""

from pathlib import Path

import pandas as pd

PROCESSED_DIR = Path("data/processed")
FEATURE_DIR = Path("data/feature_store")

FEATURE_DIR.mkdir(parents=True, exist_ok=True)


def create_user_features():

    reviews = pd.read_csv(PROCESSED_DIR / "reviews.csv")

    user_col = "user_id"
    rating_col = "rating"

    user_features = (
        reviews.groupby(user_col)
        .agg(
            activity_count=(user_col, "count"),
            average_rating=(rating_col, "mean")
        )
        .reset_index()
    )

    user_features.to_csv(
        FEATURE_DIR / "user_features.csv",
        index=False
    )

    print("[OK] user_features.csv")


def create_product_features():

    reviews = pd.read_csv(PROCESSED_DIR / "reviews.csv")

    product_col = "product_id"
    rating_col = "rating"

    product_features = (
        reviews.groupby(product_col)
        .agg(
            review_count=(product_col, "count"),
            average_rating=(rating_col, "mean")
        )
        .reset_index()
    )

    product_features.to_csv(
        FEATURE_DIR / "product_features.csv",
        index=False
    )

    print("[OK] product_features.csv")


def main():

    create_user_features()
    create_product_features()

    print("\nFeature engineering completed.")


if __name__ == "__main__":
    main()

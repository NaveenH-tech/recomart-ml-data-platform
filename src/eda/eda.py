"""
Exploratory Data Analysis (EDA)

This module generates visualizations and summary statistics
for the processed RecoMart datasets.
"""

from pathlib import Path

import pandas as pd

from src.eda.plots import (
    plot_missing_values,
    plot_category_distribution,
    plot_price_distribution,
    plot_rating_distribution,
    plot_age_distribution,
    plot_membership_distribution,
    plot_session_duration,
    plot_device_distribution,
    plot_traffic_source,
    plot_top_products,
    plot_top_users,
    plot_interaction_distribution,
    plot_interaction_heatmap,
    plot_correlation_matrix,
)

from src.eda.statistics import (
    generate_summary,
    calculate_sparsity,
)


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def load_datasets():
    """Load processed datasets."""

    products = pd.read_csv(PROCESSED_DIR / "products.csv")
    reviews = pd.read_csv(PROCESSED_DIR / "reviews.csv")
    users = pd.read_csv(PROCESSED_DIR / "users.csv")
    sessions = pd.read_csv(PROCESSED_DIR / "sessions.csv")
    clickstream = pd.read_csv(PROCESSED_DIR / "clickstream.csv")

    return products, reviews, users, sessions, clickstream


def main():

    print("=" * 60)
    print("Running Exploratory Data Analysis")
    print("=" * 60)

    (
        products,
        reviews,
        users,
        sessions,
        clickstream,
    ) = load_datasets()

    # --------------------------------------------------
    # Dataset Summary
    # --------------------------------------------------

    generate_summary(
        products,
        reviews,
        users,
        sessions,
        clickstream,
        REPORT_DIR,
    )

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    plot_missing_values(
        products,
        reviews,
        users,
        sessions,
        clickstream,
        FIGURE_DIR,
    )

    # --------------------------------------------------
    # Products
    # --------------------------------------------------

    plot_category_distribution(products, FIGURE_DIR)

    plot_price_distribution(products, FIGURE_DIR)

    plot_rating_distribution(products, FIGURE_DIR)

    plot_top_products(reviews, FIGURE_DIR)

    # --------------------------------------------------
    # Users
    # --------------------------------------------------

    plot_age_distribution(users, FIGURE_DIR)

    plot_membership_distribution(users, FIGURE_DIR)

    plot_top_users(reviews, FIGURE_DIR)

    # --------------------------------------------------
    # Sessions
    # --------------------------------------------------

    plot_session_duration(sessions, FIGURE_DIR)

    plot_device_distribution(sessions, FIGURE_DIR)

    plot_traffic_source(sessions, FIGURE_DIR)

    # --------------------------------------------------
    # Interactions
    # --------------------------------------------------

    plot_interaction_distribution(reviews, FIGURE_DIR)

    plot_interaction_heatmap(reviews, FIGURE_DIR)

    calculate_sparsity(reviews, REPORT_DIR)

    # --------------------------------------------------
    # Correlation
    # --------------------------------------------------

    plot_correlation_matrix(products, FIGURE_DIR)

    print("\nEDA Completed Successfully.")
    print(f"Reports saved to: {REPORT_DIR}")


if __name__ == "__main__":
    main()

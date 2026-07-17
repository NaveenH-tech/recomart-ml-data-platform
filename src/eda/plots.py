
"""
plots.py
Visualization utilities for RecoMart EDA.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def create_figure(figsize=(8, 5)):
    plt.figure(figsize=figsize)


def save_plot(filename: str, figure_dir: Path):
    plt.tight_layout()
    plt.savefig(figure_dir / filename, dpi=300)
    plt.close()


def plot_missing_values(products, reviews, users, sessions, clickstream, figure_dir):
    datasets = {
        "products": products,
        "reviews": reviews,
        "users": users,
        "sessions": sessions,
        "clickstream": clickstream,
    }
    for name, df in datasets.items():
        create_figure((10, 4))
        df.isnull().sum().plot(kind="bar")
        plt.title(f"Missing Values - {name.title()}")
        plt.ylabel("Count")
        save_plot(f"{name}_missing_values.png", figure_dir)


def plot_category_distribution(products, figure_dir):
    create_figure((10, 5))
    products["category"].value_counts().plot(kind="bar")
    plt.title("Category Distribution")
    plt.ylabel("Products")
    save_plot("category_distribution.png", figure_dir)


def plot_price_distribution(products, figure_dir):
    create_figure()
    products["price"].hist(bins=30)
    plt.title("Price Distribution")
    plt.xlabel("Normalized Price")
    plt.ylabel("Frequency")
    save_plot("price_distribution.png", figure_dir)


def plot_rating_distribution(products, figure_dir):
    create_figure()
    products["avg_rating"].hist(bins=20)
    plt.title("Rating Distribution")
    plt.xlabel("Normalized Rating")
    plt.ylabel("Frequency")
    save_plot("rating_distribution.png", figure_dir)


def plot_age_distribution(users, figure_dir):
    create_figure()
    users["age"].hist(bins=20)
    plt.title("Age Distribution")
    plt.xlabel("Normalized Age")
    plt.ylabel("Frequency")
    save_plot("age_distribution.png", figure_dir)


def plot_membership_distribution(users, figure_dir):
    create_figure()
    users["membership"].value_counts().plot(kind="bar")
    plt.title("Membership Distribution")
    plt.ylabel("Users")
    save_plot("membership_distribution.png", figure_dir)


def plot_session_duration(sessions, figure_dir):
    create_figure()
    sessions["session_duration_sec"].hist(bins=30)
    plt.title("Session Duration Distribution")
    plt.xlabel("Normalized Duration")
    plt.ylabel("Sessions")
    save_plot("session_duration_distribution.png", figure_dir)


def plot_device_distribution(sessions, figure_dir):
    create_figure()
    sessions["device"].value_counts().plot(kind="bar")
    plt.title("Device Distribution")
    plt.ylabel("Sessions")
    save_plot("device_distribution.png", figure_dir)


def plot_traffic_source(sessions, figure_dir):
    create_figure()
    sessions["traffic_source"].value_counts().plot(kind="bar")
    plt.title("Traffic Source Distribution")
    plt.ylabel("Sessions")
    save_plot("traffic_source_distribution.png", figure_dir)


def plot_top_products(reviews, figure_dir):
    create_figure((10,5))
    reviews["product_id"].value_counts().head(20).plot(kind="bar")
    plt.title("Top 20 Most Reviewed Products")
    plt.ylabel("Reviews")
    save_plot("top_products.png", figure_dir)


def plot_top_users(reviews, figure_dir):
    create_figure((10,5))
    reviews["user_id"].value_counts().head(20).plot(kind="bar")
    plt.title("Top 20 Most Active Users")
    plt.ylabel("Interactions")
    save_plot("top_users.png", figure_dir)


def plot_interaction_distribution(reviews, figure_dir):
    create_figure()
    reviews.groupby("user_id").size().hist(bins=30)
    plt.title("User Interaction Distribution")
    plt.xlabel("Interactions per User")
    plt.ylabel("Users")
    save_plot("interaction_distribution.png", figure_dir)


def plot_interaction_heatmap(reviews, figure_dir):
    pivot = reviews.pivot_table(index="user_id", columns="product_id",
                                values="rating", aggfunc="mean").fillna(0)
    create_figure((10,8))
    plt.imshow(pivot.iloc[:50, :50], aspect="auto")
    plt.colorbar()
    plt.title("User-Product Interaction Heatmap")
    plt.xlabel("Products")
    plt.ylabel("Users")
    save_plot("interaction_heatmap.png", figure_dir)


def plot_correlation_matrix(products, figure_dir):
    corr = products.select_dtypes(include="number").corr()
    create_figure((8,6))
    plt.imshow(corr, aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Correlation Matrix")
    save_plot("correlation_matrix.png", figure_dir)

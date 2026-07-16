"""
Train and log the recommendation model using MLflow.
"""

from pathlib import Path

import mlflow
import pandas as pd

from src.models.popularity_recommender import get_top_products

PROCESSED_DIR = Path("data/processed")


def train():

    mlflow.set_experiment("RecoMart Recommendation")

    with mlflow.start_run():

        recommendations = get_top_products(10)

        mlflow.log_param("model_type", "Popularity")

        mlflow.log_param("top_n", 10)

        mlflow.log_metric(
            "recommended_products",
            len(recommendations)
        )

        output = "reports/top10_products.csv"

        recommendations.to_csv(output, index=False)

        mlflow.log_artifact(output)

        print("Model logged successfully.")


if __name__ == "__main__":
    train()

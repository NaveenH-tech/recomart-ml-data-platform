"""
Basic data cleaning and preprocessing.
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

FILES = [
    "products.csv",
    "reviews.csv",
    "users.csv",
    "sessions.csv",
    "clickstream.csv",
]


def preprocess(file_name: str):

    df = pd.read_csv(RAW_DIR / file_name)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows where every column is missing
    df = df.dropna(how="all")

    # Fill missing values
    for column in df.columns:

        if df[column].dtype == "object":
            df[column] = df[column].fillna("Unknown")
        else:
            df[column] = df[column].fillna(0)

    output = PROCESSED_DIR / file_name
    df.to_csv(output, index=False)

    print(f"[OK] {file_name}")


def main():

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for file in FILES:
        preprocess(file)

    print("\nData preprocessing completed.")


if __name__ == "__main__":
    main()

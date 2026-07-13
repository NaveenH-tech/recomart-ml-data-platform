"""
Ingest CSV datasets into the Raw Data layer.
"""

from pathlib import Path
import shutil


SOURCE_DIR = Path("data/source")
RAW_DIR = Path("data/raw")

DATASETS = [
    "products.csv",
    "reviews.csv",
    "users.csv",
    "sessions.csv",
    "clickstream.csv",
]


def ingest_csv_files():
    """Copy CSV files into the raw data folder."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for file_name in DATASETS:

        source_file = SOURCE_DIR / file_name
        destination_file = RAW_DIR / file_name

        if not source_file.exists():
            print(f"[WARNING] {file_name} not found.")
            continue

        shutil.copy2(source_file, destination_file)
        print(f"[OK] {file_name}")


if __name__ == "__main__":
    ingest_csv_files()

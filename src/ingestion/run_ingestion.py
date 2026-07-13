"""
Master script to execute all ingestion jobs.
"""

from ingestion.csv_ingestion import ingest_csv_files
from ingestion.api_ingestion import ingest_products


def run():
    print("=" * 50)
    print("RecoMart Data Ingestion Pipeline")
    print("=" * 50)

    print("\nStep 1: CSV Ingestion")
    ingest_csv_files()

    print("\nStep 2: External API Ingestion")
    ingest_products()

    print("\nData ingestion completed successfully.")


if __name__ == "__main__":
    run()

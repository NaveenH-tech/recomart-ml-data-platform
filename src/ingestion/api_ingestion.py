"""
Ingest product data from DummyJSON API.
"""

from pathlib import Path
import requests
import json


API_URL = "https://dummyjson.com/products"
OUTPUT_FILE = Path("data/raw/external_products.json")


def ingest_products():
    """Fetch products from DummyJSON API and save as raw JSON."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Downloaded {len(data['products'])} products")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    ingest_products()

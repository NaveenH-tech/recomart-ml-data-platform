"""
Load raw CSV and JSON data into SQLite.
"""

from pathlib import Path
import json
import sqlite3

import pandas as pd

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/warehouse/recomart.db")


def load_csv(table_name: str, file_name: str, conn):
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        print(f"[WARNING] {file_name} not found.")
        return

    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"[OK] Loaded {table_name}")


def load_external_products(conn):
    file_path = RAW_DIR / "external_products.json"

    if not file_path.exists():
        print("[WARNING] external_products.json not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["products"])
    df.to_sql("external_products", conn, if_exists="replace", index=False)

    print("[OK] Loaded external_products")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    load_csv("products", "products.csv", conn)
    load_csv("reviews", "reviews.csv", conn)
    load_csv("users", "users.csv", conn)
    load_csv("sessions", "sessions.csv", conn)
    load_csv("clickstream", "clickstream.csv", conn)

    load_external_products(conn)

    conn.close()

    print("\nSQLite database created successfully.")


if __name__ == "__main__":
    main()

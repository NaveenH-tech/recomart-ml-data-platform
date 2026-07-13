"""
Basic data validation using pandas.
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_FILE = REPORT_DIR / "data_validation_report.csv"

FILES = [
    "products.csv",
    "reviews.csv",
    "users.csv",
    "sessions.csv",
    "clickstream.csv",
]


def validate_file(file_name: str):

    df = pd.read_csv(RAW_DIR / file_name)

    return {
        "dataset": file_name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def main():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for file in FILES:
        results.append(validate_file(file))

    report = pd.DataFrame(results)

    report.to_csv(REPORT_FILE, index=False)

    print(report)
    print(f"\nValidation report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()

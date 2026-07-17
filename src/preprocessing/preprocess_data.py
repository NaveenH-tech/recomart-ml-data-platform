"""
Dataset-specific preprocessing pipeline for RecoMart.
"""

from pathlib import Path

import pandas as pd

from src.preprocessing.cleaning import (
    remove_duplicates,
    fill_missing_text,
    fill_missing_boolean,
)
from src.preprocessing.encoding import encode_columns
from src.preprocessing.normalization import normalize_columns
from src.preprocessing.datetime_features import extract_datetime_features
from src.preprocessing.utils import load_csv, save_csv

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


summary = []


def log(dataset, duplicates_removed, encoded, normalized):
    summary.append({
        "dataset": dataset,
        "duplicates_removed": duplicates_removed,
        "encoded_columns": ", ".join(encoded),
        "normalized_columns": ", ".join(normalized)
    })


# ---------------------------------------------------------
# Products
# ---------------------------------------------------------

print("Processing products...")

df = load_csv(RAW_DIR / "products.csv")

df, dup = remove_duplicates(df, subset=["product_id"])

df = fill_missing_text(df, "description", "No Description")
df = fill_missing_text(df, "brand", "Unknown")
df = fill_missing_text(df, "category", "Unknown")

encoded = ["category", "brand", "availability"]
normalized = [
    "price",
    "avg_rating",
    "rating_count",
    "bestseller_rank",
]

df, _ = encode_columns(df, encoded)
df = normalize_columns(df, normalized)

save_csv(df, PROCESSED_DIR / "products.csv")

log("products", dup, encoded, normalized)

# ---------------------------------------------------------
# Convert text fields to numeric
# ---------------------------------------------------------

# Example: "4.6 out of 5 stars" -> 4.6
df["avg_rating"] = (
    df["avg_rating"]
    .astype(str)
    .str.extract(r"([0-9]+\.?[0-9]*)")[0]
)
df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")

# Example: "1,654 ratings" -> 1654
df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"([0-9]+)")[0]
)
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

encoded = ["category", "brand", "availability"]

normalized = [
    "price",
    "avg_rating",
    "rating_count",
    "bestseller_rank",
]

# ---------------------------------------------------------
# Reviews
# ---------------------------------------------------------

print("Processing reviews...")

df = load_csv(RAW_DIR / "reviews.csv")

df, dup = remove_duplicates(df, subset=["review_id"])

df = fill_missing_text(df, "review_text", "No Review")
df = fill_missing_text(df, "sentiment", "Neutral")
df = fill_missing_boolean(df, "verified_purchase", False)

encoded = ["sentiment", "verified_purchase"]
normalized = []

df, _ = encode_columns(df, encoded)

df = extract_datetime_features(df, "review_date")

save_csv(df, PROCESSED_DIR / "reviews.csv")

log("reviews", dup, encoded, normalized)


# ---------------------------------------------------------
# Users
# ---------------------------------------------------------

print("Processing users...")

df = load_csv(RAW_DIR / "users.csv")

df, dup = remove_duplicates(df, subset=["user_id"])

df = fill_missing_text(df, "gender", "Unknown")
df = fill_missing_text(df, "city", "Unknown")
df = fill_missing_text(df, "membership", "Basic")
df = fill_missing_text(df, "preferred_category", "Unknown")
df = fill_missing_text(df, "customer_segment", "Unknown")

encoded = [
    "gender",
    "city",
    "membership",
    "preferred_category",
    "customer_segment",
    "is_active",
]

normalized = ["age"]

df, _ = encode_columns(df, encoded)
df = normalize_columns(df, normalized)

df = extract_datetime_features(df, "signup_date")

save_csv(df, PROCESSED_DIR / "users.csv")

log("users", dup, encoded, normalized)


# ---------------------------------------------------------
# Sessions
# ---------------------------------------------------------

print("Processing sessions...")

df = load_csv(RAW_DIR / "sessions.csv")

df, dup = remove_duplicates(df, subset=["session_id"])

df = fill_missing_text(df, "browser", "Unknown")
df = fill_missing_text(df, "traffic_source", "Direct")

encoded = [
    "device",
    "browser",
    "traffic_source",
    "bounce",
    "conversion",
]

normalized = [
    "session_duration_sec",
    "pages_visited",
]

df, _ = encode_columns(df, encoded)
df = normalize_columns(df, normalized)

df = extract_datetime_features(df, "session_start")

save_csv(df, PROCESSED_DIR / "sessions.csv")

log("sessions", dup, encoded, normalized)


# ---------------------------------------------------------
# Clickstream
# ---------------------------------------------------------

print("Processing clickstream...")

df = load_csv(RAW_DIR / "clickstream.csv")

df, dup = remove_duplicates(df, subset=["event_id"])

df = fill_missing_text(df, "page", "Unknown")

encoded = [
    "event_type",
    "page",
    "device",
    "browser",
    "traffic_source",
    "recommendation_flag",
]

normalized = [
    "dwell_time_sec",
]

df, _ = encode_columns(df, encoded)
df = normalize_columns(df, normalized)

df = extract_datetime_features(df, "event_timestamp")

save_csv(df, PROCESSED_DIR / "clickstream.csv")

log("clickstream", dup, encoded, normalized)


# ---------------------------------------------------------
# Save preprocessing summary
# ---------------------------------------------------------

summary_df = pd.DataFrame(summary)
summary_df.to_csv(
    REPORT_DIR / "preprocessing_summary.csv",
    index=False,
)

print("\nPreprocessing completed successfully.")
print(f"Summary written to {REPORT_DIR/'preprocessing_summary.csv'}")

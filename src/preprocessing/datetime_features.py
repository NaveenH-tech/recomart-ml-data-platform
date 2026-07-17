"""
Date feature extraction.
"""

import pandas as pd


def extract_datetime_features(df, column):

    if column not in df.columns:
        return df

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    prefix = column.replace("_date", "").replace("_timestamp", "")

    df[f"{prefix}_year"] = df[column].dt.year
    df[f"{prefix}_month"] = df[column].dt.month
    df[f"{prefix}_weekday"] = df[column].dt.weekday
    df[f"{prefix}_hour"] = df[column].dt.hour

    return df

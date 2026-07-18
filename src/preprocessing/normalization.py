"""
Normalization utilities.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def normalize_columns(df, columns):
    """
    Normalize selected numeric columns using MinMaxScaler.
    """

    scaler = MinMaxScaler()

    existing = [col for col in columns if col in df.columns]

    if not existing:
        return df

    # Convert all selected columns to numeric
    for col in existing:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace NaN values with 0
    df[existing] = df[existing].fillna(0)

    # Normalize
    df[existing] = scaler.fit_transform(df[existing])

    return df
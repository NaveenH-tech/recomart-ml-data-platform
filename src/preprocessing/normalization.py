"""
Normalization utilities.
"""

from sklearn.preprocessing import MinMaxScaler


def normalize_columns(df, columns):
    scaler = MinMaxScaler()

    existing = [c for c in columns if c in df.columns]

    if existing:
        df[existing] = scaler.fit_transform(df[existing])

    return df

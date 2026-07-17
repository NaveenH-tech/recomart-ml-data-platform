"""
Categorical encoding utilities.
"""

from sklearn.preprocessing import LabelEncoder


def encode_columns(df, columns):
    encoders = {}

    for col in columns:
        if col in df.columns:
            encoder = LabelEncoder()

            df[col] = (
                df[col]
                .astype(str)
                .fillna("Unknown")
            )

            df[col] = encoder.fit_transform(df[col])

            encoders[col] = encoder

    return df, encoders

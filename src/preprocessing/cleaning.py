"""
Data cleaning utilities.
"""

import pandas as pd


def remove_duplicates(df: pd.DataFrame, subset=None):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates(subset=subset)
    removed = before - len(df)
    return df, removed


def fill_missing_text(df: pd.DataFrame, column: str, default_value: str):
    if column in df.columns:
        df[column] = df[column].fillna(default_value)
    return df


def fill_missing_numeric(df: pd.DataFrame, column: str, default_value=0):
    if column in df.columns:
        df[column] = df[column].fillna(default_value)
    return df


def fill_missing_boolean(df: pd.DataFrame, column: str, default_value=False):
    if column in df.columns:
        df[column] = df[column].fillna(default_value)
    return df

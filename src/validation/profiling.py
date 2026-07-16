from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "source"
REPORT_DIR = PROJECT_ROOT / "reports" / "data_profiling"
DOCS_DIR = PROJECT_ROOT / "docs"


# ---------------------------------------------------------
# Dataset configuration
# ---------------------------------------------------------

DATASETS = {
    "users": {
        "file": "users.csv",
        "date_columns": ["signup_date"],
    },
    "products": {
        "file": "products.csv",
        "date_columns": [],
    },
    "sessions": {
        "file": "sessions.csv",
        "date_columns": [
            "session_start",
            "session_end",
        ],
    },
    "clickstream": {
        "file": "clickstream.csv",
        "date_columns": ["event_timestamp"],
    },
    "reviews": {
        "file": "reviews.csv",
        "date_columns": ["review_date"],
    },
}


# ---------------------------------------------------------
# Profile one dataset
# ---------------------------------------------------------

def profile_dataset(
    dataset_name: str,
    file_name: str,
    date_columns: list[str],
) -> tuple[dict, pd.DataFrame]:
    """
    Read one CSV file and generate dataset-level and
    column-level profiling information.
    """

    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    dataset_summary = {
        "dataset": dataset_name,
        "file_name": file_name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            3,
        ),
    }

    column_profiles = []

    for column in df.columns:
        series = df[column]

        profile = {
            "dataset": dataset_name,
            "column": column,
            "dtype": str(series.dtype),
            "non_null_count": int(series.notna().sum()),
            "missing_count": int(series.isna().sum()),
            "missing_percentage": round(
                series.isna().mean() * 100,
                2,
            ),
            "unique_count": int(
                series.nunique(dropna=True)
            ),
            "duplicate_value_count": int(
                series.duplicated(keep=False).sum()
            ),
            "profile_type": None,
            "minimum": None,
            "maximum": None,
            "mean": None,
            "median": None,
            "invalid_date_count": None,
            "blank_string_count": None,
        }

        # Profile datetime columns
        if column in date_columns:
            parsed_dates = pd.to_datetime(
                series,
                errors="coerce",
            )

            invalid_date_mask = (
                series.notna()
                & parsed_dates.isna()
            )

            profile.update({
                "profile_type": "datetime",
                "invalid_date_count": int(
                    invalid_date_mask.sum()
                ),
                "minimum": (
                    parsed_dates.min()
                    if parsed_dates.notna().any()
                    else None
                ),
                "maximum": (
                    parsed_dates.max()
                    if parsed_dates.notna().any()
                    else None
                ),
            })

        # Profile numeric columns
        elif pd.api.types.is_numeric_dtype(series):
            numeric_values = series.dropna()

            profile.update({
                "profile_type": "numeric",
                "minimum": (
                    numeric_values.min()
                    if not numeric_values.empty
                    else None
                ),
                "maximum": (
                    numeric_values.max()
                    if not numeric_values.empty
                    else None
                ),
                "mean": (
                    round(
                        float(numeric_values.mean()),
                        3,
                    )
                    if not numeric_values.empty
                    else None
                ),
                "median": (
                    numeric_values.median()
                    if not numeric_values.empty
                    else None
                ),
            })

        # Profile text and categorical columns
        else:
            text_values = (
                series.dropna()
                .astype(str)
            )

            blank_string_count = int(
                text_values.str.strip().eq("").sum()
            )

            profile.update({
                "profile_type": "text",
                "blank_string_count": blank_string_count,
            })

        column_profiles.append(profile)

    return (
        dataset_summary,
        pd.DataFrame(column_profiles),
    )


# ---------------------------------------------------------
# Generate Markdown report
# ---------------------------------------------------------

def create_markdown_report(
    dataset_summaries: list[dict],
    column_profiles: pd.DataFrame,
) -> str:
    """
    Generate a readable Markdown profiling report.
    """

    lines = [
        "# RecoMart Data Profiling Report",
        "",
        (
            "This report summarizes dataset size, missing values, "
            "duplicate records, data types, cardinality, numerical "
            "statistics, and date coverage."
        ),
        "",
        "## 1. Dataset Summary",
        "",
        (
            "| Dataset | File | Rows | Columns | Missing Cells | "
            "Duplicate Rows | Memory MB |"
        ),
        "|---|---|---:|---:|---:|---:|---:|",
    ]

    for summary in dataset_summaries:
        lines.append(
            f"| {summary['dataset']} "
            f"| `{summary['file_name']}` "
            f"| {summary['rows']:,} "
            f"| {summary['columns']:,} "
            f"| {summary['missing_cells']:,} "
            f"| {summary['duplicate_rows']:,} "
            f"| {summary['memory_mb']} |"
        )

    # Missing-value section
    lines.extend([
        "",
        "## 2. Missing Values",
        "",
        "| Dataset | Column | Missing Count | Missing Percentage |",
        "|---|---|---:|---:|",
    ])

    missing_rows = column_profiles[
        column_profiles["missing_count"] > 0
    ]

    if missing_rows.empty:
        lines.append(
            "| All datasets | None | 0 | 0.00% |"
        )
    else:
        for _, row in missing_rows.iterrows():
            lines.append(
                f"| {row['dataset']} "
                f"| `{row['column']}` "
                f"| {int(row['missing_count']):,} "
                f"| {row['missing_percentage']:.2f}% |"
            )

    # Duplicate-row section
    lines.extend([
        "",
        "## 3. Duplicate Rows",
        "",
        "| Dataset | Duplicate Rows |",
        "|---|---:|",
    ])

    for summary in dataset_summaries:
        lines.append(
            f"| {summary['dataset']} "
            f"| {summary['duplicate_rows']:,} |"
        )

    # Column-level section
    lines.extend([
        "",
        "## 4. Column Profiles",
        "",
        (
            "| Dataset | Column | Profile Type | Pandas Type | "
            "Non-null | Missing | Unique | Minimum | Maximum | "
            "Mean | Median |"
        ),
        (
            "|---|---|---|---|---:|---:|---:|"
            "---|---|---:|---:|"
        ),
    ])

    for _, row in column_profiles.iterrows():
        minimum = (
            ""
            if pd.isna(row["minimum"])
            else str(row["minimum"])
        )

        maximum = (
            ""
            if pd.isna(row["maximum"])
            else str(row["maximum"])
        )

        mean = (
            ""
            if pd.isna(row["mean"])
            else str(row["mean"])
        )

        median = (
            ""
            if pd.isna(row["median"])
            else str(row["median"])
        )

        lines.append(
            f"| {row['dataset']} "
            f"| `{row['column']}` "
            f"| {row['profile_type']} "
            f"| {row['dtype']} "
            f"| {int(row['non_null_count']):,} "
            f"| {int(row['missing_count']):,} "
            f"| {int(row['unique_count']):,} "
            f"| {minimum} "
            f"| {maximum} "
            f"| {mean} "
            f"| {median} |"
        )

    # Invalid date section
    lines.extend([
        "",
        "## 5. Date Profiling",
        "",
        (
            "| Dataset | Column | Invalid Dates | "
            "Earliest Date | Latest Date |"
        ),
        "|---|---|---:|---|---|",
    ])

    date_rows = column_profiles[
        column_profiles["profile_type"] == "datetime"
    ]

    for _, row in date_rows.iterrows():
        invalid_count = (
            0
            if pd.isna(row["invalid_date_count"])
            else int(row["invalid_date_count"])
        )

        lines.append(
            f"| {row['dataset']} "
            f"| `{row['column']}` "
            f"| {invalid_count:,} "
            f"| {row['minimum']} "
            f"| {row['maximum']} |"
        )

    # Blank-string section
    lines.extend([
        "",
        "## 6. Blank String Checks",
        "",
        "| Dataset | Column | Blank Strings |",
        "|---|---|---:|",
    ])

    text_rows = column_profiles[
        column_profiles["profile_type"] == "text"
    ]

    blank_rows_found = False

    for _, row in text_rows.iterrows():
        blank_count = (
            0
            if pd.isna(row["blank_string_count"])
            else int(row["blank_string_count"])
        )

        if blank_count > 0:
            blank_rows_found = True

            lines.append(
                f"| {row['dataset']} "
                f"| `{row['column']}` "
                f"| {blank_count:,} |"
            )

    if not blank_rows_found:
        lines.append(
            "| All datasets | None | 0 |"
        )

    lines.extend([
        "",
        "## 7. Generated Outputs",
        "",
        "- `reports/data_profiling/dataset_summary.csv`",
        "- `reports/data_profiling/column_profiles.csv`",
        "- `docs/data_profile.md`",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------
# Main execution
# ---------------------------------------------------------

def main() -> None:
    """
    Profile all configured datasets and save the reports.
    """

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Raw data directory: {RAW_DIR}")
    print()

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset_summaries = []
    all_column_profiles = []

    for dataset_name, config in DATASETS.items():
        print(f"Profiling {dataset_name}...")

        summary, column_profile = profile_dataset(
            dataset_name=dataset_name,
            file_name=config["file"],
            date_columns=config["date_columns"],
        )

        dataset_summaries.append(summary)
        all_column_profiles.append(column_profile)

    summary_df = pd.DataFrame(
        dataset_summaries
    )

    columns_df = pd.concat(
        all_column_profiles,
        ignore_index=True,
    )

    dataset_summary_file = (
        REPORT_DIR / "dataset_summary.csv"
    )

    column_profiles_file = (
        REPORT_DIR / "column_profiles.csv"
    )

    markdown_file = (
        DOCS_DIR / "data_profile.md"
    )

    summary_df.to_csv(
        dataset_summary_file,
        index=False,
    )

    columns_df.to_csv(
        column_profiles_file,
        index=False,
    )

    markdown_report = create_markdown_report(
        dataset_summaries=dataset_summaries,
        column_profiles=columns_df,
    )

    markdown_file.write_text(
        markdown_report,
        encoding="utf-8",
    )

    print()
    print("Profiling completed successfully.")
    print(f"Dataset summary: {dataset_summary_file}")
    print(f"Column profiles: {column_profiles_file}")
    print(f"Markdown report: {markdown_file}")


if __name__ == "__main__":
    main()
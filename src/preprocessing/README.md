# Data Preprocessing

## Objective

The preprocessing module cleans the raw datasets and prepares them for Exploratory Data Analysis (EDA) and Feature Engineering.

## Input

The module reads the following datasets from the raw data layer:

- products.csv
- reviews.csv
- users.csv
- sessions.csv
- clickstream.csv

Location:

```
data/raw/
```

## Preprocessing Steps

The current implementation performs the following operations:

1. Remove duplicate records.
2. Remove rows where all values are missing.
3. Fill missing values:
   - Text columns → "Unknown"
   - Numeric columns → 0

## Output

Cleaned datasets are stored in:

```
data/processed/
```

Files generated:

- products.csv
- reviews.csv
- users.csv
- sessions.csv
- clickstream.csv

## Execution

Run the preprocessing pipeline using:

```bash
python -m src.preprocessing.preprocess_data
```

## Expected Output

```
[OK] products.csv
[OK] reviews.csv
[OK] users.csv
[OK] sessions.csv
[OK] clickstream.csv

Data preprocessing completed.
```

## Next Stage

The processed datasets are used for:

- Exploratory Data Analysis (EDA)
- Feature Engineering
- Recommendation Model Training

# Feature Engineering

## Objective

Create features suitable for recommendation algorithms, such as: 1. User activity frequency 2. Average rating per user/item 3. Co-occurrence or similarity-based features.
Store transformed data in a structured database or warehouse.

## Input

The module reads the following datasets from the processed data layer:

- products.csv
- reviews.csv
- users.csv
- sessions.csv

Location:

```
data/processed/
```

## Preprocessing Steps

The current implementation performs the following operations:

1. User activity frequency .
2. Average rating per user/item .
3. Cosine Similarity
3. Fill missing values:
   - Text columns → "Unknown"
   - Numeric columns → 0

## Output

Store transformed data in a warehouse database.

```
sqllite database tables
dim_users
dim_products
fact_interactions
item_similarity
```

- Users Loaded            : 3,000
- Products Loaded         : 728
- Interactions Loaded     : 6,327
- Similarity Records      : 489,300

## Execution

Run the preprocessing pipeline using:

```bash
python src/feature_engineering/feature_runner.py
or 
python -m src.feature_engineering.feature_runner
```

## Expected Output

```
TASK 6 FEATURE ENGINEERING COMPLETED
=================================================================
Users Loaded            : 3,000
Products Loaded         : 728
Interactions Loaded     : 6,327
Similarity Records      : 489,300
Warehouse Database      : /workspaces/recomart-ml-data-platform/data/warehouse/recomart_warehouse.db


```




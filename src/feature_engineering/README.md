# Feature Engineering

## Objective

Create recommendation-ready features from processed datasets to support collaborative filtering and recommendation algorithms.
The feature engineering pipeline generates:
1.User Activity Frequency
2.Average Rating per User
3.Average Rating per Item
4.Item Popularity Metrics
5.Clickstream-Based Behavioral Features
6.Cosine Similarity-Based Features
Structured Warehouse Tables for Model Training and Analytics
The transformed data is stored in a structured SQLite warehouse for downstream machine learning and recommendation workflows..

## Input

The module reads the following datasets from the processed data layer:

- products.csv
- reviews.csv
- users.csv
- sessions.csv
- clickstream.csv

Location:

```
data/processed/
```

## Preprocessing & Processing Steps

Before feature engineering and warehouse loading, the pipeline performs several preprocessing and validation operations to ensure data quality, consistency, and reliable feature generation.
# 1. Input File Validation
The pipeline verifies that all required source datasets are available.
users.csv
products.csv
reviews.csv
sessions.csv
clickstream.csv
# 2. Validation Logic
File exists
File is accessible
File is not empty
# 3. Error Example
FileNotFoundError:
Missing input files:
['data/processed/clickstream
# 4. Schema Validation
The pipeline validates mandatory columns in each dataset before processing.
# 5. Data Type Standardization
Several clickstream columns are converted into numeric format before aggregation.
# 6. Missing Value Handling
The pipeline handles missing values before generating features.
# 7. Session-Based Aggregation
Input
session_id   user_id
S1           U001
S2           U001
S3           U002
Output
user_id   user_activity_frequency
U001      2
U002      1
# 8. Review-Based Aggregation
# 9. Clickstream Feature Aggregation
# 10. Similarity Computation
# 11. Timestamp Generation
# 12. Warehouse Loading and Validation

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




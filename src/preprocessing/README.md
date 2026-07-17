# Step 5 – Data Preparation & Exploratory Data Analysis (EDA)

## Objective

The objective of this phase is to prepare the raw datasets for machine learning by performing data cleaning, preprocessing, normalization, feature encoding, and exploratory data analysis (EDA). The processed datasets generated in this step will serve as inputs for feature engineering and recommendation model development.

---

# Dataset Overview

The project uses six datasets.

| Dataset | Description |
|----------|-------------|
| products.csv | Product catalog information |
| reviews.csv | User-product ratings and reviews |
| users.csv | Customer demographic information |
| sessions.csv | Website session details |
| clickstream.csv | User browsing events |
| external_api.json | External product metadata |

---

# Project Structure

```
RecoMart-ML-Data-Platform/

├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   ├── figures/
│   ├── preprocessing_summary.csv
│   ├── interaction_statistics.csv
│   └── eda_summary.md
│
└── src/
    ├── preprocessing/
    │   ├── __init__.py
    │   ├── preprocess_data.py
    │   ├── cleaning.py
    │   ├── encoding.py
    │   ├── normalization.py
    │   ├── datetime_features.py
    │   └── utils.py
    │
    └── eda/
        ├── __init__.py
        ├── eda.py
        ├── plots.py
        └── statistics.py
```

---

# Data Preprocessing

The preprocessing pipeline converts raw datasets into machine learning ready datasets.

The following operations are performed.

## 1. Duplicate Removal

Duplicate records are removed using the primary key of each dataset.

| Dataset | Duplicate Key |
|----------|---------------|
| Products | product_id |
| Reviews | review_id |
| Users | user_id |
| Sessions | session_id |
| Clickstream | event_id |

---

## 2. Missing Value Handling

Missing values are handled using domain-specific defaults.

Examples include:

- Missing descriptions → "No Description"
- Missing brand/category → "Unknown"
- Missing review text → "No Review"
- Missing browser → "Unknown"
- Missing traffic source → "Direct"

---

## 3. Data Cleaning

Certain columns required additional preprocessing.

### Product Ratings

Example

```
4.6 out of 5 stars
```

Converted to

```
4.6
```

### Rating Count

Example

```
1,654 ratings
```

Converted to

```
1654
```

This ensures numerical columns can be normalized correctly.

---

## 4. Label Encoding

Categorical variables are converted into numerical representations.

Examples include

- category
- brand
- availability
- gender
- membership
- preferred_category
- customer_segment
- device
- browser
- traffic_source
- sentiment
- verified_purchase

---

## 5. Normalization

Numerical features are normalized using MinMaxScaler.

Normalized columns include

Products

- price
- avg_rating
- rating_count
- bestseller_rank

Users

- age

Sessions

- session_duration_sec
- pages_visited

Clickstream

- dwell_time_sec

---

## 6. Date Feature Extraction

Additional temporal features are extracted.

Examples

Review Date

- Year
- Month
- Weekday

Signup Date

- Year
- Month

Session Start

- Hour
- Weekday

Event Timestamp

- Hour
- Weekday

---

# Processed Files

The preprocessing pipeline generates

```
products_processed.csv

reviews_processed.csv

users_processed.csv

sessions_processed.csv

clickstream_processed.csv
```

---

# Exploratory Data Analysis

The EDA module helps understand the characteristics of the processed datasets.

The following analyses are performed.

## Dataset Summary

- Number of rows
- Number of columns
- Missing values
- Duplicate records
- Numerical statistics

---

## Distribution Analysis

Generated plots include

- Missing Values
- Product Category Distribution
- Price Distribution
- Rating Distribution
- User Age Distribution
- Membership Distribution
- Session Duration Distribution
- Device Distribution
- Traffic Source Distribution

---

## User Behaviour Analysis

Visualizations include

- Top 20 Most Active Users
- Top 20 Most Reviewed Products
- User Interaction Distribution
- User-Product Interaction Heatmap

---

## Correlation Analysis

A correlation matrix is generated for all numerical product features.

---

## Dataset Sparsity

Interaction sparsity is calculated using

```
Sparsity = 1 − (Observed Interactions / Possible Interactions)
```

where

```
Possible Interactions

=

Number of Users × Number of Products
```

The statistics are stored in

```
interaction_statistics.csv
```

---

# Generated Reports

```
reports/

├── figures/
│
├── preprocessing_summary.csv
│
├── interaction_statistics.csv
│
└── eda_summary.md
```

---

# Execution

## Run Preprocessing

```bash
python src/preprocessing/preprocess_data.py
```

---

## Run EDA

```bash
python src/eda/eda.py
```

---

# Output

After execution

```
data/processed/
```

contains cleaned datasets

and

```
reports/
```

contains

- summary report
- interaction statistics
- EDA figures

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

---

# Learning Outcome

This phase transforms raw transactional datasets into structured machine learning datasets by performing preprocessing, cleaning, encoding, normalization, feature extraction, and exploratory data analysis.

The processed datasets generated in this step serve as the foundation for feature engineering, feature store creation, recommendation model development, and model training in the subsequent phases of the project.

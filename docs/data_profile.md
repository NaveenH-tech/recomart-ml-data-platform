# RecoMart Data Profiling Report

This report summarizes dataset size, missing values, duplicate records, data types, cardinality, numerical statistics, and date coverage.

## 1. Dataset Summary

| Dataset | File | Rows | Columns | Missing Cells | Duplicate Rows | Memory MB |
|---|---|---:|---:|---:|---:|---:|
| users | `users.csv` | 3,000 | 9 | 0 | 0 | 1.993 |
| products | `products.csv` | 728 | 10 | 253 | 0 | 1.327 |
| sessions | `sessions.csv` | 15,000 | 11 | 0 | 0 | 7.08 |
| clickstream | `clickstream.csv` | 122,114 | 12 | 0 | 0 | 71.736 |
| reviews | `reviews.csv` | 6,327 | 8 | 77 | 0 | 3.308 |

## 2. Missing Values

| Dataset | Column | Missing Count | Missing Percentage |
|---|---|---:|---:|
| products | `category` | 13 | 1.79% |
| products | `price` | 21 | 2.88% |
| products | `avg_rating` | 9 | 1.24% |
| products | `rating_count` | 9 | 1.24% |
| products | `availability` | 13 | 1.79% |
| products | `bestseller_rank` | 188 | 25.82% |
| reviews | `rating` | 7 | 0.11% |
| reviews | `review_text` | 39 | 0.62% |
| reviews | `review_date` | 31 | 0.49% |

## 3. Duplicate Rows

| Dataset | Duplicate Rows |
|---|---:|
| users | 0 |
| products | 0 |
| sessions | 0 |
| clickstream | 0 |
| reviews | 0 |

## 4. Column Profiles

| Dataset | Column | Profile Type | Pandas Type | Non-null | Missing | Unique | Minimum | Maximum | Mean | Median |
|---|---|---|---|---:|---:|---:|---|---|---:|---:|
| users | `user_id` | text | object | 3,000 | 0 | 3,000 |  |  |  |  |
| users | `age` | numeric | int64 | 3,000 | 0 | 43 | 18 | 60 | 38.757 | 38.0 |
| users | `gender` | text | object | 3,000 | 0 | 2 |  |  |  |  |
| users | `city` | text | object | 3,000 | 0 | 6 |  |  |  |  |
| users | `membership` | text | object | 3,000 | 0 | 3 |  |  |  |  |
| users | `preferred_category` | text | object | 3,000 | 0 | 140 |  |  |  |  |
| users | `signup_date` | datetime | object | 3,000 | 0 | 1,105 | 2022-01-01 00:00:00 | 2025-04-15 00:00:00 |  |  |
| users | `customer_segment` | text | object | 3,000 | 0 | 4 |  |  |  |  |
| users | `is_active` | numeric | bool | 3,000 | 0 | 2 | False | True | 0.742 | 1.0 |
| products | `product_id` | text | object | 728 | 0 | 728 |  |  |  |  |
| products | `product_name` | text | object | 728 | 0 | 704 |  |  |  |  |
| products | `category` | text | object | 715 | 13 | 140 |  |  |  |  |
| products | `brand` | text | object | 728 | 0 | 285 |  |  |  |  |
| products | `price` | numeric | float64 | 707 | 21 | 505 | 5.4573 | 249.99 | 35.324 | 28.95 |
| products | `avg_rating` | text | object | 719 | 9 | 24 |  |  |  |  |
| products | `rating_count` | text | object | 719 | 9 | 645 |  |  |  |  |
| products | `availability` | text | object | 715 | 13 | 11 |  |  |  |  |
| products | `bestseller_rank` | numeric | float64 | 540 | 188 | 260 | 1.0 | 994.0 | 174.622 | 56.5 |
| products | `description` | text | object | 728 | 0 | 697 |  |  |  |  |
| sessions | `session_id` | text | object | 15,000 | 0 | 15,000 |  |  |  |  |
| sessions | `user_id` | text | object | 15,000 | 0 | 2,980 |  |  |  |  |
| sessions | `session_start` | datetime | object | 15,000 | 0 | 13,670 | 2025-01-01 08:06:00 | 2025-03-31 22:57:00 |  |  |
| sessions | `session_end` | datetime | object | 15,000 | 0 | 14,972 | 2025-01-01 08:17:00 | 2025-03-31 23:15:19 |  |  |
| sessions | `device` | text | object | 15,000 | 0 | 3 |  |  |  |  |
| sessions | `browser` | text | object | 15,000 | 0 | 4 |  |  |  |  |
| sessions | `traffic_source` | text | object | 15,000 | 0 | 5 |  |  |  |  |
| sessions | `session_duration_sec` | numeric | int64 | 15,000 | 0 | 1,741 | 60 | 1800 | 932.242 | 934.0 |
| sessions | `pages_visited` | numeric | int64 | 15,000 | 0 | 17 | 2 | 18 | 10.013 | 10.0 |
| sessions | `bounce` | numeric | int64 | 15,000 | 0 | 2 | 0 | 1 | 0.035 | 0.0 |
| sessions | `conversion` | numeric | bool | 15,000 | 0 | 2 | False | True | 0.352 | 0.0 |
| clickstream | `event_id` | numeric | int64 | 122,114 | 0 | 122,114 | 1 | 122114 | 61057.5 | 61057.5 |
| clickstream | `session_id` | text | object | 122,114 | 0 | 15,000 |  |  |  |  |
| clickstream | `user_id` | text | object | 122,114 | 0 | 2,980 |  |  |  |  |
| clickstream | `product_id` | text | object | 122,114 | 0 | 728 |  |  |  |  |
| clickstream | `event_timestamp` | datetime | object | 122,114 | 0 | 120,539 | 2025-01-01 08:07:20 | 2025-03-31 23:06:16 |  |  |
| clickstream | `event_type` | text | object | 122,114 | 0 | 9 |  |  |  |  |
| clickstream | `page` | text | object | 122,114 | 0 | 5 |  |  |  |  |
| clickstream | `device` | text | object | 122,114 | 0 | 3 |  |  |  |  |
| clickstream | `browser` | text | object | 122,114 | 0 | 4 |  |  |  |  |
| clickstream | `traffic_source` | text | object | 122,114 | 0 | 5 |  |  |  |  |
| clickstream | `dwell_time_sec` | numeric | int64 | 122,114 | 0 | 176 | 5 | 180 | 92.33 | 92.0 |
| clickstream | `recommendation_flag` | numeric | int64 | 122,114 | 0 | 2 | 0 | 1 | 0.067 | 0.0 |
| reviews | `review_id` | text | object | 6,327 | 0 | 6,327 |  |  |  |  |
| reviews | `user_id` | text | object | 6,327 | 0 | 2,611 |  |  |  |  |
| reviews | `product_id` | text | object | 6,327 | 0 | 700 |  |  |  |  |
| reviews | `rating` | numeric | float64 | 6,320 | 7 | 5 | 1.0 | 5.0 | 4.533 | 5.0 |
| reviews | `review_text` | text | object | 6,288 | 39 | 6,182 |  |  |  |  |
| reviews | `sentiment` | numeric | float64 | 6,327 | 0 | 3,054 | -1.0 | 1.0 | 0.308 | 0.3 |
| reviews | `verified_purchase` | numeric | bool | 6,327 | 0 | 2 | False | True | 0.975 | 1.0 |
| reviews | `review_date` | datetime | object | 6,296 | 31 | 627 | 2013-01-13 00:00:00 | 2025-03-09 00:00:00 |  |  |

## 5. Date Profiling

| Dataset | Column | Invalid Dates | Earliest Date | Latest Date |
|---|---|---:|---|---|
| users | `signup_date` | 0 | 2022-01-01 00:00:00 | 2025-04-15 00:00:00 |
| sessions | `session_start` | 0 | 2025-01-01 08:06:00 | 2025-03-31 22:57:00 |
| sessions | `session_end` | 0 | 2025-01-01 08:17:00 | 2025-03-31 23:15:19 |
| clickstream | `event_timestamp` | 0 | 2025-01-01 08:07:20 | 2025-03-31 23:06:16 |
| reviews | `review_date` | 0 | 2013-01-13 00:00:00 | 2025-03-09 00:00:00 |

## 6. Blank String Checks

| Dataset | Column | Blank Strings |
|---|---|---:|
| All datasets | None | 0 |

## 7. Generated Outputs

- `reports/data_profiling/dataset_summary.csv`
- `reports/data_profiling/column_profiles.csv`
- `docs/data_profile.md`

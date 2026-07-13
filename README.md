# RecoMart ML Data Platform

End-to-end Data Management Pipeline for Machine Learning.

## Course

BITS Pilani

Data Management for Machine Learning

## Team

GRP-32 DMML

## Business Problem

RecoMart is an e-commerce startup that wants to build a scalable recommendation system.

The objective is to build an end-to-end production-quality ML Data Platform covering

- Data Ingestion
- Data Validation
- Data Preparation
- Feature Engineering
- Feature Store
- Data Versioning
- Recommendation Models
- MLflow
- Airflow Orchestration

## Tech Stack

Python 3.11

Pandas

SQLite

Great Expectations

Feast

DVC

MLflow

Apache Airflow

Scikit-Learn

Plotly

Matplotlib

## Repository Structure
<p>
recomart-ml-data-platform/
│
├── config/
│   ├── config.yaml
│   └── logging.yaml
│
├── data/
│   ├── raw/
│   ├── validated/
│   ├── processed/
│   ├── warehouse/
│   ├── external/
│   └── feature_store/
│
├── docs/
│
├── logs/
│
├── mlruns/
│
├── notebooks/
│
├── reports/
│
├── src/
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   │
│   ├── ingestion/
│   ├── validation/
│   ├── preprocessing/
│   ├── eda/
│   ├── feature_engineering/
│   ├── feature_store/
│   ├── models/
│   ├── evaluation/
│   └── orchestration/
│
├── tests/
│
├── health_check.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── Makefile
├── dvc.yaml
├── .gitignore
└── LICENSE
</p>
## Quick Start

pip install -r requirements.txt

python health_check.py

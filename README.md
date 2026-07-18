# RecoMart ML Data Platform

An end-to-end Data Management pipeline for Machine Learning that powers a scalable product recommendation system for an e-commerce platform.

---

## Course

**BITS Pilani – Work Integrated Learning Programme**

**Data Management for Machine Learning (DMML)**

---

## Team

**Group 32**

---

## Problem Statement

RecoMart is an e-commerce startup that wants to build a scalable and maintainable recommendation platform.

The system continuously ingests user behaviour, product metadata, transactional information and external API data, validates and prepares datasets, engineers reusable features, trains recommendation models, and tracks ML experiments through an orchestrated data pipeline.

---

## Pipeline Overview

```
Data Sources
(CSV + REST API)
        │
        ▼
Data Ingestion
        │
        ▼
Raw Data Storage
        │
        ▼
Data Validation
        │
        ▼
Data Preparation
        │
        ▼
Feature Engineering
        │
        ▼
SQLite Warehouse
        │
        ▼
Feature Store
        │
        ▼
Recommendation Models
        │
        ▼
MLflow Tracking
        │
        ▼
Workflow Orchestration
```

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Data Processing | Pandas |
| Database | SQLite |
| Data Validation | Great Expectations |
| Feature Store | Feast |
| Data Versioning | DVC |
| Experiment Tracking | MLflow |
| Workflow Orchestration | Prefect *(or Apache Airflow)* |
| Machine Learning | Scikit-Learn |
| Visualisation | Matplotlib, Plotly |

---

# Repository Structure

```
recomart-ml-data-platform/
│
├── config/                  # Configuration files
│   ├── config.yaml
│   └── logging.yaml
│
├── data/
│   ├── source/                 # Raw ingested datasets
│   ├── validated/           # Quality-checked datasets
│   ├── processed/           # Cleaned & transformed datasets
│   ├── warehouse/           # SQLite warehouse
│   ├── external/            # API responses
│   └── feature_store/       # Feature store assets
│
├── docs/                    # Documentation
├── logs/                    # Application logs
├── mlruns/                  # MLflow experiment tracking
├── notebooks/               # Exploratory analysis
├── reports/                 # Validation & evaluation reports
│
├── src/
│   ├── common/              # Shared utilities
│   ├── ingestion/           # Data collection & ingestion
│   ├── validation/          # Data profiling & validation
│   ├── preprocessing/       # Data cleaning & preparation
│   ├── feature_engineering/ # Feature generation
│   ├── feature_store/       # Feature registry
│   ├── models/              # Recommendation models
│   ├── evaluation/          # Model evaluation
│   └── orchestration/       # Workflow orchestration
│
├── tests/                   # Unit tests
│
├── requirements.txt
├── README.md
├── dvc.yaml
├── Makefile                 # Optional automation commands
└── .gitignore
```

---

## Getting Started

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

(Optional) Verify the environment

```bash
python health_check.py
```

Run the pipeline

```bash
python src/orchestration/<pipeline_entrypoint>.py
```

---

## Project Setup

### Prerequisites

Ensure the following software is installed before running the project:

- Python 3.11+
- Git
- Git Large File Storage (Git LFS)

Install project dependencies:

```bash
pip install -r requirements.txt
```

Initialize Git LFS (one-time setup):

```bash
git lfs install
```

After cloning the repository, download all LFS-managed datasets and artifacts:

```bash
git lfs pull
```

Run the environment verification script:

```bash
python health_check.py
```

The project uses **Git LFS** to manage large datasets and binary artifacts such as source datasets, processed data, and SQLite warehouse files, ensuring the Git repository remains lightweight while supporting reproducible data pipelines.

---

## Key Features

- Multi-source data ingestion from CSV files and REST APIs
- Immutable raw data storage with layered data architecture
- Automated data validation and quality assessment
- Data preparation and feature engineering pipeline
- Structured SQLite data warehouse for analytics and ML
- Centralized feature management using a Feature Store
- Recommendation model training and evaluation
- Experiment tracking with MLflow
- End-to-end pipeline orchestration
- Modular, configurable, and extensible architecture

---

## License

This project has been developed for academic purposes as part of the BITS Pilani WILP programme.

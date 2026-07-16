from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="recomart_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id="ingest",
        bash_command="python -m src.ingestion.run_ingestion",
    )

    validate = BashOperator(
        task_id="validate",
        bash_command="python -m src.validation.validate_data",
    )

    preprocess = BashOperator(
        task_id="preprocess",
        bash_command="python -m src.preprocessing.preprocess_data",
    )

    features = BashOperator(
        task_id="feature_engineering",
        bash_command="python -m src.feature_engineering.generate_features",
    )

    model = BashOperator(
        task_id="train_model",
        bash_command="python -m src.models.train_model",
    )

    ingest >> validate >> preprocess >> features >> model

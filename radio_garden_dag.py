from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

# Garante que o diretório das DAGs está no PYTHONPATH
sys.path.append(os.path.join(os.environ["AIRFLOW_HOME"], "dags"))

from radio_garden.extract_stations import extract_stations
from radio_garden.transform_stations import transform_stations
from radio_garden.load_to_minio import load_to_minio

# Caminhos locais
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

# Default args para o DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 10, 27),
    "retries": 1,
}

# Define o DAG
with DAG(
    dag_id="radio_garden_pipeline",
    default_args=default_args,
    description="Pipeline ETL para o projeto Radio Garden",
    schedule_interval=None,  # Executa apenas manualmente (pode mudar depois)
    catchup=False,
    tags=["radio", "etl", "minio"],
) as dag:

    # Tarefa 1 - Extração
    extract_task = PythonOperator(
        task_id="extract_stations",
        python_callable=extract_stations,
        op_args=[RAW_DIR],
    )

    # Tarefa 2 - Transformação
    transform_task = PythonOperator(
        task_id="transform_stations",
        python_callable=transform_stations,
        op_args=[RAW_DIR, PROCESSED_DIR],
    )

    # Tarefa 3 - Load para o MinIO
    load_task = PythonOperator(
        task_id="load_to_minio",
        python_callable=load_to_minio,
        op_args=[PROCESSED_DIR, "radio-garden", "stations.json"],
    )

    # Define a ordem das tarefas
    extract_task >> transform_task >> load_task

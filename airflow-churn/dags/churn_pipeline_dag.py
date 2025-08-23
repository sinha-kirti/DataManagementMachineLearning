from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Explicitly add the absolute path to the parent directory of DataIngestion
sys.path.append("/Users/kirtisinha/DataManagementMachineLearning")

from DataIngestion.ingestion import ingest
from DataValidation.validation import validate_data_and_generate_report
from DataTransformationAndStorage.transformation import transform_data as transform
from ModelBuilding.model import train_model
from datetime import datetime

def ingest():
    print("Ingesting raw data...")
    ingest()

def validate():
    print("Validating data...")
    sources = r"/Users/kirtisinha/DataManagementMachineLearning/DataIngestion/data_raw"
    validation_report = "data_validation_report1.xlsx"
    validate_data_and_generate_report(sources, validation_report)

def transform():
    print("Transforming data...")
    # transform()

def train():
    print("Training churn model...")
    train_model()

with DAG(
    dag_id="churn_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    ingest_task = PythonOperator(task_id="ingest", python_callable=ingest)
    validate_task = PythonOperator(task_id="validate", python_callable=validate)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    train_task = PythonOperator(task_id="train", python_callable=train)

    ingest_task >> validate_task >> transform_task >> train_task
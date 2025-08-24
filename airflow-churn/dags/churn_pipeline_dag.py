from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Explicitly add the absolute path to the parent directory of DataIngestion
sys.path.append("/Users/kirtisinha/DataManagementMachineLearning")

from DataIngestion.ingestion import ingest
from DataValidation.validation import validate_data_and_generate_json_report, get_latest_date_folder
from DataTransformationAndStorage.transformation import transform_data
from ModelBuilding.model import train_model
from datetime import datetime

def ingest():
    print("Ingesting raw data...")
    ingest()

def validate():
    print("Validating data...")
    data_raw_dir = "/opt/airflow/project/DataIngestion/data_raw"
    validation_report = "/opt/airflow/project/data_validation_report.json"

    # Define sources dynamically
    sources = {}
    for source in ["github", "kaggle"]:
        source_dir = os.path.join(data_raw_dir, source)
        latest_date = get_latest_date_folder(source_dir)
        if latest_date:
            if source == "github":
                file_path = os.path.join(source_dir, latest_date, "IBM_Telco_Customer_Churn.csv")
            else:
                file_path = os.path.join(source_dir, latest_date, "WA_Fn-UseC_-Telco-Customer-Churn.csv")
            sources[source] = file_path

    # Use the new JSON-based validation method
    validate_data_and_generate_json_report(sources, validation_report)

def transform():
    print("Transforming data...")
    # Call the data transformation script
    transform_data()

def train():
    print("Training churn model...")
    # Call the train script
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
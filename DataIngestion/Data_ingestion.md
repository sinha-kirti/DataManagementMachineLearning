# 🔹 Step 1 – Data Ingestion

## Objective
Collect raw data from source systems and load it into the pipeline for further processing.

## Process
- Source dataset: *Telco Customer Churn dataset* (CSV format).  
- Data ingested into Airflow DAG using `PythonOperator`.  
- Data stored in a staging area before further steps.

## Implementation Highlights
- Uses **pandas** for reading CSVs.  
- Modular ingestion function supports multiple file types (CSV, Excel, JSON).  
- Logs ingestion success/failure in Airflow.  

## Challenges & Solutions
- **Challenge:** Handling multiple file formats.  
  **Solution:** Created ingestion script with parameterized readers.  

- **Challenge:** Large CSVs taking time to load.  
  **Solution:** Used chunk loading in pandas for scalability.  

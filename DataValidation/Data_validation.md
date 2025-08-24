# 🔹 Step 4 – Data Validation

## Objective
Ensure that the dataset is accurate, complete, and reliable before feature engineering and model training.

## Validation Checks
- **Schema Validation:** Column names, data types.  
- **Completeness:** Mandatory fields (e.g., `customerID`).  
- **Range Checks:** Example – `MonthlyCharges > 0`.  
- **Uniqueness:** No duplicate customer IDs.  
- **Statistical Validation:** Compare distributions to historical data (drift detection).  

## Implementation Highlights
- Validation script runs as an Airflow task.  
- Failures trigger alerts and stop pipeline.  
- Logs validation results for audit.  

## Challenges & Solutions
- **Challenge:** Schema drift when dataset evolved.  
  **Solution:** Added schema comparison function with alerts.  

- **Challenge:** Unexpected nulls in mandatory fields.  
  **Solution:** Applied data quality rules and fail-fast mechanism.  

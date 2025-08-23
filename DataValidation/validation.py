import os
import pandas as pd
from datetime import datetime

# Base raw data directory

data_raw_dir = os.getcwd() + "/DataIngestion/data_raw"
validation_report = "data_validation_report.xlsx"

def get_latest_date_folder(source_dir):
    """Finds the latest date folder inside a source directory."""
    try:
        date_folders = [
            d for d in os.listdir(source_dir)
            if os.path.isdir(os.path.join(source_dir, d))
        ]
        # Convert to datetime for proper sorting
        date_folders = sorted(date_folders, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        return date_folders[-1] if date_folders else None
    except Exception as e:
        print(f"⚠️ Could not fetch date folder for {source_dir}: {e}")
        return None

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

def validate_dataset(name, file_path):
    print(f"Validating {name} dataset...")

    # Load data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {"Error": str(e)}

    results = {}

    # Missing values
    missing = df.isnull().sum()
    results["MissingValues"] = missing[missing > 0]

    # Duplicates
    duplicates = df.duplicated().sum()
    results["Duplicates"] = pd.Series([duplicates], index=["Duplicate Rows"])

    # Data types
    dtypes = df.dtypes
    results["DataTypes"] = dtypes

    # Negative values (numeric columns only)
    # Negative values (numeric columns only)
    negatives = {}
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            negatives[col] = neg_count

    results["NegativeValues"] = pd.Series(negatives, dtype="int64")


    return results

def validate_data_and_generate_report(sources, report_file):
    with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
        has_data = False  # Track if any sheet has data
        for name, path in sources.items():
            results = validate_dataset(name, path)
            if "Error" in results:
                pd.DataFrame({"Error": [results["Error"]]}).to_excel(writer, sheet_name=f"{name}_Error")
                has_data = True
                continue

            # Always write each check (even if empty)
            for check_name, data in results.items():
                if isinstance(data, pd.Series):
                    df = data.to_frame(name="Value")
                elif isinstance(data, pd.DataFrame):
                    df = data
                else:
                    df = pd.DataFrame({"Result": [str(data)]})  # fallback

                # If no rows, create a message row
                if df.empty:
                    df = pd.DataFrame({"Message": [f"No {check_name} issues found"]})

                df.to_excel(writer, sheet_name=f"{name}_{check_name}")
                has_data = True

        # Add a default sheet if no data was written
        if not has_data:
            pd.DataFrame({"Message": ["No validation data available"]}).to_excel(writer, sheet_name="Summary")


# Run validation
validate_data_and_generate_report(sources, validation_report)

import os
import logging
import pandas as pd
from datetime import datetime

# ---------------- Config ----------------
BASE_RAW_DIR = "data_raw"
LOG_DIR = "logs"

KAGGLE_DATASET = "palashfendarkar/wa-fnusec-telcocustomerchurn"
KAGGLE_CSV = "WA_Fn-UseC_-Telco-Customer-Churn.csv"

IBM_CSV_URL = "https://github.com/IBM/telco-customer-churn-on-icp4d/raw/master/data/Telco-Customer-Churn.csv"
IBM_CSV_FILE = "IBM_Telco_Customer_Churn.csv"

# Current date for versioned folders
DATE_FOLDER = datetime.now().strftime("%Y-%m-%d")

# ---------------- Setup ----------------
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ---------------- Download Kaggle dataset ----------------
def download_kaggle_dataset():
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()

        kaggle_dir = os.path.join(BASE_RAW_DIR, "kaggle", DATE_FOLDER)
        os.makedirs(kaggle_dir, exist_ok=True)

        logging.info(f"Starting Kaggle dataset Ingestion")
        api.dataset_download_files(KAGGLE_DATASET, path=kaggle_dir, unzip=True)
        logging.info(f"Downloaded Kaggle dataset to {kaggle_dir}")

    except Exception as e:
        logging.error(f"Failed to download Kaggle dataset: {e}")
        raise

# ---------------- Download IBM dataset ----------------
def download_ibm_dataset():
    try:
        ibm_dir = os.path.join(BASE_RAW_DIR, "github", DATE_FOLDER)
        os.makedirs(ibm_dir, exist_ok=True)

        logging.info(f"Starting GitHub dataset Ingestion")
        df = pd.read_csv(IBM_CSV_URL)
        ibm_path = os.path.join(ibm_dir, IBM_CSV_FILE)
        df.to_csv(ibm_path, index=False)

        logging.info(f"Downloaded GitHub dataset to {ibm_dir}")

    except Exception as e:
        logging.error(f"Failed to download GitHub dataset: {e}")
        raise

# ---------------- Main ----------------
def ingest():
    try:
        download_kaggle_dataset()
        download_ibm_dataset()
        print(f"Both datasets downloaded under {BASE_RAW_DIR}/<source>/{DATE_FOLDER}/")
        logging.info("Ingestion complete.")
    except Exception as e:
        print("Ingestion failed:", e)

if __name__ == "__main__":
    ingest()

# Data Management and Machine Learning Pipeline

This repository contains a comprehensive end-to-end machine learning pipeline for customer churn prediction, incorporating data management best practices, automated workflows, and model deployment capabilities.

## Project Structure

```
├── airflow-churn/          # Airflow DAGs and configuration for pipeline automation
├── DataIngestion/          # Data collection and initial processing
├── DataPreparation/        # Data cleaning and preprocessing
├── DataTransformationAndStorage/  # Data transformation and storage logic
├── DataValidation/         # Data quality checks and validation
├── FeatureStore/          # Feature engineering and storage
├── ModelBuilding/         # Model training, evaluation, and selection
└── RawDataStorage/        # Initial data storage layer
```

## Features

- **Automated Data Pipeline**: Using Apache Airflow for orchestration
- **Data Quality Management**: Comprehensive validation and monitoring
- **Feature Engineering**: Systematic feature creation and storage
- **Model Training**: Multiple models (LogisticRegression, RandomForest) with performance tracking
- **Docker Integration**: Containerized workflow with docker-compose
- **Visualization**: Data distribution and model performance plots

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- DuckDB
- Required Python packages (specified in requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sinha-kirti/DataManagementMachineLearning.git
cd DataManagementMachineLearning
```

2. Create and activate a virtual environment:
```bash
python -m venv dmml
source dmml/bin/activate  # On Windows: dmml\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Airflow services:
```bash
cd airflow-churn
docker-compose up
```

## Pipeline Components

### 1. Data Ingestion
- Sources data from multiple sources (GitHub, Kaggle)
- Handles raw data storage and initial processing
- Logs all ingestion activities

### 2. Data Preparation
- Implements data cleaning procedures
- Generates distribution plots and correlation analysis
- Creates cleaned datasets for further processing

### 3. Data Transformation & Storage
- Transforms data into required format
- Utilizes DuckDB for efficient storage
- Implements data versioning

### 4. Data Validation
- Performs quality checks
- Validates data consistency
- Generates validation reports

### 5. Feature Store
- Manages feature engineering
- Stores and versions features
- Ensures feature consistency

### 6. Model Building
- Trains multiple model types
- Tracks model performance
- Stores trained models with timestamps

## Monitoring and Logging

- Comprehensive logging system across all components
- Performance tracking for models
- Data quality monitoring
- Pipeline execution logs

## Model Performance

Latest model performance metrics are available in:
- `ModelBuilding/model_performance_20250823.csv`
- Visual results in `DataPreparation/Results/`

## Documentation

Detailed documentation for each component is available in their respective directories:
- Data Ingestion: `DataIngestion/Data_ingestion.md`
- Data Preparation: `DataPreparation/Data_preparation.md`
- Data Transformation: `DataTransformationAndStorage/Data_transformation_storage.md`
- Data Validation: `DataValidation/Data_validation.md`
- Feature Store: `FeatureStore/Feature_store.md`
- Model Building: `ModelBuilding/Model_building.md`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Kirti Sinha - 2024da04194@wilp.bits-pilani.ac.in
Chandana Bonagiri - 2024da04196@wilp.bits-pilani.ac.in
Vadde Praveen - 2024da04203@wilp.bits-pilani.ac.in


Project Link: https://github.com/sinha-kirti/DataManagementMachineLearning

# E-Commerce-Data-Engineering-Analytics-System
---

# End-to-End ETL and ML Pipeline with Airflow and Spark

This project runs a full data engineering and machine learning workflow using Python, PostgreSQL, MongoDB, Apache Spark, and Airflow.

## Pipeline Order

1. **salesdb/main.py** - Generates RDBMS data and exports to CSV
2. **catalogdb/main.py** - Extracts MongoDB product catalog and flattens it
3. **dw/main.py** - Builds a dimensional warehouse and loads the data
4. **MLOPS/model.py** - Trains a sales forecasting model using PySpark
5. **MLOPS/predict.py** - Loads the model and makes predictions

## Folder Structure

- `salesdb/`: Contains RDBMS data generation and extraction logic
- `catalogdb/`: Extracts data from MongoDB and flattens JSON
- `dw/`: Loads and transforms staging data into a PostgreSQL data warehouse
- `MLOPS/`: Contains Spark ML training and prediction logic
- `elt_dag.py`: Airflow DAG to orchestrate the complete pipeline

## Prerequisites

- Python 3.10+
- PostgreSQL
- MongoDB
- PySpark
- Airflow (optional for automation)
- JDBC Driver (`postgresql-42.x.x.jar`)
- Java installed and configured

## Setup

Set up each `.env` with DB credentials, ports, and paths.

## Running the Pipeline

You can either:
- Run scripts manually in order
- Or use the `etl_dag.py` with Apache Airflow for orchestration

## Deployment

1. Clone this repo
2. Configure your `.env` files
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

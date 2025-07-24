
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
}

dag = DAG(
    dag_id='sales_to_ml_pipeline',
    default_args=default_args,
    description='Run ETL then ML prediction pipeline',
    schedule_interval=None,  # run manually or as needed
    catchup=False
)

BASE_PATH = '/path/to/your/project'  # change this to your actual base path

def run_script(script_path):
    full_path = os.path.join(BASE_PATH, script_path)
    subprocess.run(['python', full_path], check=True)

sales_task = PythonOperator(
    task_id='run_salesdb_main',
    python_callable=run_script,
    op_args=['salesdb/main.py'],
    dag=dag
)

catalog_task = PythonOperator(
    task_id='run_catalogdb_main',
    python_callable=run_script,
    op_args=['catalogdb/main.py'],
    dag=dag
)

dw_task = PythonOperator(
    task_id='run_dw_main',
    python_callable=run_script,
    op_args=['dw/main.py'],
    dag=dag
)

model_task = PythonOperator(
    task_id='run_model_training',
    python_callable=run_script,
    op_args=['MLOPS/model.py'],
    dag=dag
)

predict_task = PythonOperator(
    task_id='run_model_prediction',
    python_callable=run_script,
    op_args=['MLOPS/predict.py'],
    dag=dag
)

# Task dependencies
sales_task >> catalog_task >> dw_task >> model_task >> predict_task

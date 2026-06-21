import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args={
    'email': ['robin2662883@gmail.com'],
    'email-on_failure': False,
    'email_on_retry': False,
    'start_date': datetime.datetime(2025, 12, 1),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5)
}

dag=DAG('employee_data', default_args=default_args, description='runs an external python script',schedule='*/10 * * * *', max_active_runs=2, catchup=False, dagrun_timeout= datetime.timedelta(minutes=10))

with dag:
    run_python_script=BashOperator (task_id='extract_data', bash_command='python /home/airflow/gcs/dags/extract.py') #Airflow DAG folder path

    start_pipeline = CloudDataFusionStartPipelineOperator(
    location="us-central1",
    pipeline_name="etl-pipeline",
    instance_name="datafusion-dev",
    pipeline_timeout=1000,
    task_id="start_datafusion_pipeline")

    run_python_script >> start_pipeline

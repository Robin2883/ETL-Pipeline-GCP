import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

def hello():
    print("hello world")

default_args={
    'start_date': datetime.datetime(2025, 12, 1),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5)
}

dag=DAG('basic_dag', default_args=default_args, description='basic dag',schedule='*/10 * * * *', max_active_runs=2, catchup=False, dagrun_timeout= datetime.timedelta(minutes=10))

bash_operator=BashOperator (task_id='echo', bash_command='echo test', dag=dag)

python_operator=PythonOperator(task_id='hello_world', python_callable=hello, dag=dag)

bash_operator >> python_operator  #dependency
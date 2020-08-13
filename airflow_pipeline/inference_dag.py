from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

import get_new_records_for_predictions 

default_args = {
    'owner': 'EMR Appliance Pipeline',
    'start_date': datetime(2020,1,24)
}

dag = DAG('emr-inference-dag', default_args=default_args)

new_records_operator = PythonOperator(
    task_id = 'get_new_records',
    python_callable=get_new_records_for_predictions.get_records,
    dag = dag
    )

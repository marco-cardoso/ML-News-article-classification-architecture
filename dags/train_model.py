"""
    This DAG is responsible to download the latest articles and create
    an updated model.
"""
import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from news_classifier.scraper import scraper
from news_classifier.models.train_model import train

default_args = {
    "depends_on_past": False,
    "start_date": datetime.datetime(2020, 3, 5),
    "retries": 0,
    "retry_delay": datetime.timedelta(minutes=1)
}

dag = DAG(
    "update_data",
    description="Gets the daily properties using zoopla API",
    schedule_interval="0 0 * * *",
    default_args=default_args,
    catchup=False
)

t1 = PythonOperator(
    task_id="update_data",
    python_callable=scraper.main,
    dag=dag
)

t2 = PythonOperator(
    task_id="train_model",
    python_callable=train,
    dag=dag
)

t1 >> t2
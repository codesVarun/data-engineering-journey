from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
import logging
import pandas as pd

# from scripts.extract import fetch_covid_data
# from scripts.transform import transform_continent_data
# from scripts.load import load_data

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from extract import fetch_covid_data
from transform import transform_continent_data
from load import load_data

default_args = {
    'owner': 'codesVarun',
    'email': ['singhvarun9554@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='covid_api_etl',
    default_args=default_args,
    description='ETL pipeline for COVID-19 data from public API',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'covid', 'api'],
) as dag:

    def extract_task(**context):
        logging.info("🔄 Extracting COVID data from API")
        data = fetch_covid_data()
        if not data:
            raise ValueError("❌ No data fetched from API")
        context['ti'].xcom_push(key='raw_data', value=data)

    def check_data_task(**context):
        raw_data = context['ti'].xcom_pull(key='raw_data')
        if raw_data:
            return 'transform_covid_data'
        return 'no_data_branch'

    def transform_task(**context):
        raw_data = context['ti'].xcom_pull(key='raw_data')
        if not raw_data:
            raise ValueError("❌ No raw data available for transformation")
        df_continents, df_countries = transform_continent_data(raw_data)
        context['ti'].xcom_push(key='df_continents', value=df_continents.to_json(orient='records'))
        context['ti'].xcom_push(key='df_countries', value=df_countries.to_json(orient='records'))
        logging.info(f"✅ Transformed {len(df_continents)} continents & {len(df_countries)} countries")

    def load_task(**context):
        df_continents_json = context['ti'].xcom_pull(key='df_continents')
        df_countries_json = context['ti'].xcom_pull(key='df_countries')
        if not df_continents_json or not df_countries_json:
            raise ValueError("❌ Transformed data not found in XComs")
        df_continents = pd.read_json(df_continents_json, orient='records')
        df_countries = pd.read_json(df_countries_json, orient='records')
        load_data(df_continents, df_countries)
        logging.info("📥 Data loaded into database")

    def alert_no_data():
        logging.warning("⚠️ No data to process today. Skipping transform and load.")

    extract = PythonOperator(
        task_id='extract_covid_data',
        python_callable=extract_task,
    )

    check_data = BranchPythonOperator(
        task_id='check_data_validity',
        python_callable=check_data_task,
    )

    transform = PythonOperator(
        task_id='transform_covid_data',
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id='load_covid_data',
        python_callable=load_task,
    )

    no_data = PythonOperator(
        task_id='no_data_branch',
        python_callable=alert_no_data,
    )

    end = EmptyOperator(
        task_id='end_pipeline',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    # DAG execution flow
    extract >> check_data >> [transform, no_data]
    transform >> load >> end
    no_data >> end
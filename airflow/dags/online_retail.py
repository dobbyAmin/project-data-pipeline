from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator

local_tz = pendulum.timezone("Asia/Bangkok")

default_args = {
    "owner": "DE-team",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    "email": ["bi@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
}


def ingest_csv_to_postgres():
    csv_path = "/opt/airflow/dags/data/online_retail.csv"
    df = pd.read_csv(csv_path)

    mask_invoice = df["InvoiceNo"].astype(str).str.match(r"^\d", na=False)
    mask_stockcode = df["StockCode"].astype(str).str.match(r"^\d{5}", na=False)

    condition = (
        mask_invoice
        & mask_stockcode
        & df["InvoiceNo"].notna()
        & df["StockCode"].notna()
        & df["Quantity"].notna()
        & (df["Quantity"] > 0)
        & df["UnitPrice"].notna()
        & (df["UnitPrice"] > 0)
        & df["CustomerID"].notna()
    )

    df_raw = df[condition].copy()
    df_issue = df[~condition].copy()

    engine = create_engine(
        "postgresql+psycopg2://dpuser:dppass@dp_postgres:5432/project_retail"
    )

    df_raw.to_sql(
        "raw_data", con=engine, schema="staging", if_exists="replace", index=False
    )

    df_issue.to_sql(
        "data_issues", con=engine, schema="staging", if_exists="replace", index=False
    )


with DAG(
    dag_id="Online_Retail_Pipeline",
    start_date=pendulum.datetime(2025, 9, 1, tz=local_tz),
    schedule_interval="0 3 * * *",
    catchup=False,
    default_args=default_args,
    tags=["Online_Retail", "daily work"],
)as dag:

    # 1) Ingestion
    ingest_csv = PythonOperator(
        task_id="ingest_csv",
        python_callable=ingest_csv_to_postgres,
    )
    validate_staging = BashOperator(
        task_id="validate_staging",
        bash_command=(
            "cd /workspace/gx_retail && "
            "great_expectations checkpoint run raw_data_checkpoint"
        ),
        dag=dag,
    )

    # 2) Core
    dbt_run_core = BashOperator(
        task_id="dbt_run_core",
        bash_command="cd /usr/app/retail_core && dbt run --select core",
        dag=dag,)
    validate_core = BashOperator(
        task_id="validate_core",
        bash_command=(
            "cd /workspace/gx_retail && "
            "great_expectations checkpoint run core_checkpoint"
        ),
        dag=dag,
    )

    # 3) Data Marts
    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command="cd /usr/app/retail_mart && dbt run --select marts",
        dag=dag,
    )
    validate_mart_sales = BashOperator(
        task_id="validate_mart_sales",
        bash_command=(
            "cd /workspace/gx_retail && "
            "great_expectations checkpoint run mart_sales_checkpoint"
        ),
        dag=dag,
    )
    validate_mart_customer = BashOperator(
        task_id="validate_mart_customer",
        bash_command=(
            "cd /workspace/gx_retail && "
            "great_expectations checkpoint run mart_customer_checkpoint"
        ),
        dag=dag,
    )

    # 4) Publish
    publish = EmailOperator(
        task_id="publish",
        to="bi@online_retail.com",
        subject="Online Retail Data Marts are ready.",
        html_content="<h3>Online Retail Data Marts are ready for analysis.</h3>",
        dag=dag,
    )

    # DAG dependencies
    ingest_csv >> validate_staging >> dbt_run_core >> validate_core

    validate_core >> dbt_run_marts >> [validate_mart_sales, validate_mart_customer] >> publish
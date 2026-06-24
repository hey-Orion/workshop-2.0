import time 
import requests
import logging
from requests.exceptions import RequestException

def fetch_data(url: str, retries: int = 3) -> list:
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 429:
                wait_time = int (response.headers.get("retry", 5))
                logging.warning(f"rate limited")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        except RequestException as e:
            logging.error(f"attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise e 
            time.sleep(2 ** attempt)



def parse_clean(raw_records: list) -> list:
    cleaned = []
    for record in raw_records:
        if not record.get("id") or "price" not in record:
            continue

        try:
            raw_price = str(record["price"]).replace("$", "").strip()
            price = float(raw_price)
            if price <= 0:
                continue
        except (ValueError, TypeError):
            continue
        
        cleaned.append({
            "tx_id": record["id"],
            "amount": price,
            "at": int(time.time())
        })

    return cleaned



from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def email_alert(context):
    print(f"Task failed. Sending operational alert for: {context['task_instance'].task_id}")

default_args = {
    "owner": "dataops",
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
    "on_failure": email_failure_alert
}

with DAG(
    dag_id='no=1',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

check_api = BashOperator(
    task_id="check_api",
    bash_command="curl -I https://api.eu-sales.com/health"
)

def trigger_extraction():
    print("fetch_data...")

run_extraction = PythonOperator(
    task_id="runner",
    python_callable=trigger_extraction
)

check_api >> run_extraction



from airflow.decorators import task

with DAG(dag_id="dynamic_params_dag", start_date=datetime(2026, 1, 1), schedule="0 6 * * *", catchup=False) as dag:

    @task
    def extract_data(**context):
        execution_date = context["ds"]
        return {"start_date": execution_date, "end_date": execution_date}

    @task
    def run_pipeline(dates: dict):
        print(f"Processing data incrementally from {dates['start_date']} to {dates['end_date']}")

    run_pipeline(extract_date_range())



from pydantic import BaseModel, EmailStr, Field 

class UserProfile(BaseModel):
    user_id: int 
    email: EmailStr 
    vat_num: str = Field(min_length=5, max_length=15)
    account_balance: float = Field(default=0.0)

from pydantic import ValidationError

def Validate_payload(raw_json: dict):
    try:
        user = UserProfile(**raw_json)
        return user.model_dump()
    except ValidationError as e:
        print(f"data validation: {e.json}")
        return None



from sqlalchemy import create_engine
import pandas as pd 

def dump_store(df: pd.DataFrame, db_uri: str, target_table: str):

    engine = create_engine(db_uri)
    with engine.begin() as connection:
        df.to_sql(name=target_table, con=connection, if_exists="append", index=False)



def check_db(db_uri: str) -> str:
    engine = create_engine(db_uri)
    with engine.connect() as conn:
        result = conn.execute("select version();").fetchone()
        return result[0]



import pandas as pd

def merge_clean(sales_csv: str, regions_csv: str) -> pd.DataFrame:
    sales_df = pd.read_csv(sales_csv)
    regions_csv = pd.read_csv(regions_csv)

    sales_df = sales_df.dropna(subset=["id", "amount"])

    merged_df = pd.merge(sales_df, regions_csv, on="region_id", how="inner")
    return merged_df


def computer_ca(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("country_code").agg({
        "amount": "sum",
        "id": "count"
    }).rename(columns={"amount": "total_rev", "id": "order_count"})
    return summary.reset_index()

    
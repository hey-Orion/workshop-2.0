from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def say_hello():
    print("hello airflow")

with DAG(
    dag_id="hello",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False 
) as dag:

    hello_tast = PythonOperator(
        task_id="hello_task",
        python_callable=say_hello
    )



from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("API")
    
def transform():
    print("data")

def load():
    print("loading")

with DAG(
    dag_id="pipeline"
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="data",
        python_callable=transform
    )

    loadt_task = PythonOperator(
        task_id="load",
        python_callable=load
    )

    extract_task >> transform_task >> load_task



from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def get_number():
    return 10 

def multiply_by_two(ti):
    number = ti.xcom_pull(task_ids="get_number")
    print(number * 2)

with DAG(
    dag_id="xcom_example",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="get_number",
        python_callable=get_number
    )

    task2 = PythonOperator(
        task_id="multiply",
        python_callable=multiply_by_two
    )

    task1 >> task2


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def risky_task():
    raise Exception("somthing went wrong")

with DAG(
    dag_id="retry",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="risky",
        python_callable=risky,
        retries=3,
        retry_delay=timedelta(minutes=2) 
    )


from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="bash",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task = BashOperator(
        task_id="list_files",
        bash_command="ls -lah"
    )


from airflow.decorators import task

@task
def process_user(user):
    print(user) 

user = ["john", "alice", "bob"]

process_user.expand(user=users)
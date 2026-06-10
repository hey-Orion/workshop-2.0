from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class rew_data(BaseModel):
    id: int = Field(gt=0)
    email: EmailStr
    amount: float = Field(gt=0,0)
    timestamp: datetime


from pydantic import ValidationError

def payload(raw_records: list) -> tuple[list, list]:
    valid = []
    invalid = []

    for idx, raw_item in enumerate(raw_records):
        try:
            model = rew_data.model_validate(raw_item)
            valid.append(model.model_dump())
        except ValidationError as e:
            invalid.append({"index": idx, "errors": e.errors(), "raw": raw_item})
    return valid, invalid

what is enumerate, and model.model_dump(), e.errors()


import requests, time 
from requests.exceptions import RequestException 

def fetch(url: str, retries: int = 3, delay: int = 1) -> list:
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json
        except RequestException as e:
            if attempt == retries:
                raise RuntimeError("error")
            time.sleep(delay)
            delay *= 2 

explain this one line by line with code is in every line and code 


import pandas as pd 

def chunks(records: list, output_csv: srt, chunk_size: int = 2):
    df = pd.DataFrame(records)

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        chunk.to_csv(output_csv, mode='a', index=False, header=not os.path.existe(output_csv))

explain this one line by line with code is in every line and code 


import pandas as pd 

def trans_raw(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=["id"])
    df["email"] = df["email"].str.strip().str.lower()
    return df 

explain this one line by line with code is in every line and code 


with ranked_trans as (
    select id, email, amount, timestamp,
            row_number() over(
                partititon by id order by timestamp desc
            ) as rn 
    from records 
)
select id, email, amount, timestamp
from ranked_trans
where rn = 1;

i dont understand the ranked_trans loop 
explain this one line by line with code


select timestamp::date as trans_date,
        sum(amount) as total,
        avg(amount) over(
            order by timestamp::date
            rows between 2 preceding as current row 
        ) as rolling_3_day_avg
from silver_db 
group by timestamp::date, amount;

explain this block with code and  why is this used  avg(amount) over(
            order by timestamp::date
            rows between 2 preceding as current row 
        ) as rolling_3_day_avg
from silver_db 


import pytest
import pandas as pd 

@pytest.fixture
def mock_data():
    return [
        {"transaction_id": 1, "user_email": "TEST@domain.com ", "amount": 50.0, "timestamp": "2026-06-08T12:00:00"},
        {"transaction_id": 1, "user_email": "test@domain.com", "amount": 55.0, "timestamp": "2026-06-08T13:00:00"}
    ]

is the return defining the output of the fungstion ?

def test_logic(mock_data):
    valid, invalid = validate_stream_payloads(mock_data)
    assert len(valid) == 2 
    assert len(invalid) == 0 
    assert valid[0]["email"] == "123we@gamil.com "

explain this one line by line with code is in every line and code 


import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data_project")

def log_pipeline(error_message: str):
    logger.error(f"error")
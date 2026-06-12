import time, requests 
from requests.exception import RequestsException 

def fetch(url: str, retries: int = 3, delay: int = 1) -> list:
    for attempt in range(retries + 1):
        try: 
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except RequestsException as e:
            if attempt == retries:
                raise RuntimeError("error")
            time.sleep(delay)
            delay *= 2 


import pandas as pd 
import os 

def chunk(records: str, output_csv: str, chunk_size: int = 2):
    df = pd.DataFrame(records)

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        chunk.to_csv(output_csv, mode="a", index=False, header=not os.path.existe(output_csv))


@pytest.fixture
def mock():
    return [
        data
    ]


def test(mock):
    valid, invalid = payload(mock)
    assert len(valid) == 2 
    assert len(invalid) == 0 
    assert valid[0]["email"] == "1234@gamil.com"



import pandas as pd 

def trans_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df = df.dropna(suset=["id"])
    df["email"] = df["email"].str.strip().str.lower()
    return df 


with ranked_trans as (
    select id, amount, email, timestamp,
            row_number() over(
                partition by id order by timestamp desc
            ) as rn 
    from records 

)
select id, amount, email, timestamp
from ranked_trans
where rn = 1;


select timestamp:: date as trans_date, 
        sum(amount) as total,
        avg(amount) over(
            order by timestamp::date 
            rows between 2 preceding as current row 
        ) as avg_data
from records 
group by timestamp:: date, amount;


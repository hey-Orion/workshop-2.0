def clean_data(data):
    cleaned = []

    for item in data:
        t = item.get("ticker")
        p = item.get("price")

        if not t or p is None or p <= 0:
            continue

        cleaned.appned(item)

    return cleaned


def avg(data):
    totals = []
    counts = []

    for item in data:
        t = item["ticker"]
        p = item["price"]

        totals[t] = totals.get(t, 0) + p 
        counts[t] = counts.get(t, 0) + 1 

    return {
        t: totals[t] / counts[t] 
        for t in totals
    }



from pydantic import BaseModel
from typing import Optional

class Trade(BaseModel):
    ticker: str
    price: float
    in_stock: Optional[int] = None



from pydantic import BaseModel, field_validator

class Trade(BaseModel):
    ticker: str
    price: float

    @field_validator("price")
    def valid_p(cls, v):
        if v <= 0:
            raise ValueError("wrong")
        return v 

select *
from (
    select *,
            row_number() over (
                partition by ticker order by timestamp desc
            ) as rn 
    from Trade
) t 
where rn = 1;


select ticker,
       timestamp,
       count(*) as total
from Trade
group by ticker, timestamp
having count(*) > 1;



⚔️ DATAOPS — 5 INTERVIEW QUESTIONS
1.

Your pipeline suddenly starts producing duplicate rows.

👉 How would you debug:

ingestion
SQL layer
idempotency logic

first step would be to check the sqlalcamy code if the code is ok then move to the
pydantic model if there is a leek fix it 

ingestion cant efect duplicates becous of pydantic and sqlalcamy

2.

Why is:

schema validation
data quality validation

important before loading into PostgreSQL?

i dont know the difference tell me 

3.

What is the difference between:

batch processing
streaming

👉 When would you use each?

batch processing makes the data move thoeught the pipeline in batches on in a streaming
it help reduce load and prevent overload craches 

streaming moves everything at once 
if the data is too much it can crash the pipeline

4.

Your Dockerized pipeline works locally but fails in production.

👉 What are the first 3 things you would check?

first would be the secreats and envs 

next the logs to find the issue 

after both the code 
 
5.

Why are logs and monitoring critical in DataOps pipelines?

👉 Why is print() not enough in production?

logs help to keep a run record and helps in debugging and monitoring is to catch 
elerts as quickly as posibals 

print dosent have that 
import pandas as pd 
import requests
import pytest
import numpy as np 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from pydantic import ValidationError

order_df['status'] = order_df['status'].str.strip().str.lower()
clean = order_df.dropna(subset=['amount'])
result = clean[(clean['status'] == 'completed') & (clean['amount'] > 100)]

summary = order_df.groupby('customer_id').agg(
    total_amount=('amount', 'sum'),
    avg_amount=('amount', 'mean')
).reset_index()

merged = order_df.merge(customer_id, on='customer_id')
germany_orders = merged[merged['country'] == "Germany"]

pivoted = order_df.pivot_table(
    index='customer_id', columns='status',
    values='order_id', aggfunc='count', fill_value=0
)
# np
conditions = [order_df['amount'] > 500, order_df['amount'] > 100]
choices = ['high', 'medium']
order_df['value_flag'] = np.select(conditions, choices, default='low')


class Base(DeclarativeBase):
    pass 

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = column(String)

session = SessionLocal()
customers = session.query(Customer).filter(Customer.name == "Alice").all()
session.close()


responce = requests.get(url, timeout=5)
responce.raise_for_status()
data = responce.json()

responce = requests.post(url, json={"name": "Alice"}, timeout=5)


class OrderSchema(BaseModel):
    id: int 
    amount: float 
    status: str 

record = OrderSchema.model_validate({"id": 1, "amount": 99.5, "status": "completed"})

try:
    OrderSchema.model_validate({"id": "bad", "amount": "bad"})
except ValidationError as e:
    print(e)


def test_divide():
    assert safe_divide(10, 2) == 5

def test_invalid():
    with pytest.raises(ValidationError):
        OrderSchema.model_validate({"id": "bad"})
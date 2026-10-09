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

merged = order_df.merge(customers_df, on='customer_id')
germany_orders = merged[merged['country'] == 'Germany']

pivated = order_df.pivot_table(
    index='customer_id', columns='status',
    values='order_id', aggfunc='count', fill_value=0
)
# np
conditions = [order_df['amount'] > 500, order_df['amount'] > 100]
choices = ['high', 'medium']
order_df['value_flag'] = np.select(conditions, choices, default='low')


class Base(DeclarativeBase):
    pass 

class Products(Base):
    __tablename__ = 'products'
    id = column(Integer, primary_key=True)
    name = column(String)

session = SessionLocal()
products = session.query(Products).filter(Products.name == "alice").all()
session.close()


response = requests.get(url, timeout=5)
response.raise_for_status()
data = response.json()

response = requests.post(url, json={"name": "Alice"}, timeout=5)


class OrderSchema(BaseModel):
    id: int 
    amount: float
    status: str

record = OrderSchema.model_validate({"id": 1, "amount": 99.9, "status": "completed"})

try:
    OrderSchema.model_validate({"id": "bad", "amount": "bad"})
except ValidationError as e:
    print(e)


def test_safe_divide():
    assert safe_divide(10, 2) == 5

def test_invalid():
    with pytest.raise(ValidationError):
        OrderSchema.model_validate({"id": "bad"})

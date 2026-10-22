import pandas as pd 
import pytest 
import requests
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

orders = [
    {"id": 1, "amount": 50, "status": "completed"},
    {"id": 2, "amount": 120, "status": "pending"},
    {"id": 3, "amount": 80, "status": "completed"}
]

name = "hada"
print(name)

for i in range(1, 10):
    print(i)

def square(n):
    return n * n 

def records(numbers):
    if not in numbers:
        return None 
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = numbers
    return largest

def lower(strings):
    return [s.lower() for s in strings]

for order in orders:
    print(order["amount"])

def completed(orders):
    count = 0
    for item in orders:
        if item["status"] == "completed":
            count += 1 
    return count 

def count_active_orders(orders):
    return sum(1 for item in orders if item.get("status") == "active")

def count_ch(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    return counts


orders_df = pd.DataFrame(orders)

ho = orders_df.amount
print(ho)

rev = orders_df["amount"]
print(rev)

filterd_df = orders_df[orders_df["status"] == "completed"]
sorted_df = orders_df.sort_values(by="amount", ascending=False)

status_count = orders_df["status"].value_counts()
print(status_count)

orders_df.rename(columns={"amount": "total"}, inplace=True)

avg_total = orders_df["total"].mean 
print(avg_total)


url = "........."

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    _ = response.json()
except requests.exceptions.RequestException as e:
    print("error", e)


class CustomerModel(BaseModel):
    id: int 
    name: str 
    email: Optional[EmailStr] = None

customer = CustomerModel(id=1, name="nada")
print(customer)

try: 
    
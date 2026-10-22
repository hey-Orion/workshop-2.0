import pandas as pd
import pytest
import requests
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# --- 1. Basic Data Structures & Control Flow ---

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
    if not numbers:
        return None
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num 
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


# --- 2. Pandas Operations ---

orders_df = pd.DataFrame(orders)

ho = orders_df.columns
print(ho)

rev = orders_df["amount"]
print(rev)

filterd_df = orders_df[orders_df["status"] == "completed"]
sorted_df = orders_df.sort_values(by="amount", ascending=False)

status_count = orders_df['status'].value_counts()
print(status_count)

orders_df.rename(columns={"amount": "total"}, inplace=True)

avg_total = orders_df["total"].mean()
print(avg_total)


# --- 3. Requests & API Interaction ---

url = "https://httpbin.org/get"

response = requests.get(url, timeout=5)
response.raise_for_status()

print(response.status_code)
result = response.json()
print(result)

params = {"q": "python"}
headers = {"User-Agent": "my-app"}
response = requests.get("https://httpbin.org/get", params=params, headers=headers)

post_data = {"name": "hada", "id": "ascf"}
response = requests.post("https://httpbin.org/post", json=post_data, headers=headers)

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    _ = response.json()
except requests.exceptions.RequestException as e:
    print("error:", e)

session = requests.Session()
session.headers.update({"Authorization": "Bearer token123"})

response1 = session.get("https://httpbin.org/get", timeout=5)
response2 = session.get("https://httpbin.org/get", timeout=5)


# --- 4. Pydantic Models ---

class CustomerModel(BaseModel):
    id: int 
    name: str 
    email: Optional[EmailStr] = None 

customer = CustomerModel(id=1, name="hada")
print(customer)

try:
    bad_customer = CustomerModel(id="invalid_int", name="")
except ValidationError as e:
    print("Validation error caught successfully.")


# --- 5. Pytest Unit Tests ---

def test_sq():
    assert square(3) == 9

def test_count_active_orders():
    test_orders = [
        {"status": "active"},
        {"status": "pending"},
        {"status": "active"}
    ]
    result = count_active_orders(test_orders)
    assert result == 2 

def test_div():
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0 


# --- 6. SQLAlchemy Database Setup ---

engine = create_engine("sqlite:///:memory:")

class Base(DeclarativeBase):
    pass 

class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

Base.metadata.create_all(engine)

with Session(engine) as session:
    new_cus = Customer(name="yo")
    session.add(new_cus)
    session.commit()
    print("Successfully added new customer to SQLite DB.")
name = "harsh"
print(name)

for i in range(1, 10):
    print(1)

def square(n):
    return n * n 
    
def records(numbers):
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num 
    return largest

def lower(str):
    return [s.lower() for s in str]

for order in orders:
print(order["amount"])

def completed(orders):
    count = 0
    for item in orders:
        if item["status"] == "completed":
            count += 1 
    return count

def count_ch(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1 
    return counts 


import pandas as pd 
orders_df = pd.DataFrame(orders)

ho = orders_df.columns
print(ho)

rev = orders_df["amount"]
print(rev)

filterd = orders_df[orders_df["status"] == "completed"]

sorted_df = orders_df.sort_values(by="amount", ascending=False)

status_count = orders_df['status'].value_counts()
print(status_count)

orders_df.rename(columns={"amount": "total"}, inplace=True)

avg_total = orders_df['total'].mean()
print(avg_total)


import requests 

url = 'https://api.github.com'

response = requests.get(url, timeout=5)
response.raise_for_status()

print(response.status_code)

result = response.json()
print(result)

params = {"q": "python"}
headers = {"U-A": "......", "A": "....."}
response = requests.get("url", params=params, headers=headers)

post_data = {"name": "hada", "id": "ascf"}
response = requests.post("url", json=post_data, headers=headers)


import requests

try:
    response = requests.get("url", timeout=5)
    response.raise_for_status()
    response.json()
except requests.exceptions.RequestException as e:
    print("error")


import requests

session = requests.Session()

session.headers.update({"Authorization": "Bearer token123"})

response1 = session.get("url", timeout=5)
response2 = session.get("url", timeout=5)


from typing import Optional
from pydantic import BaseModel, EmailStr

class Customer(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None

customer = Customer(id=1, name="hada")
print(customer)

from pydantic import BaseModel, ValidationError

class Customer(BaseModel):
    id: int 
    name: str 

try:
    bad_customer = Customer(id="sd", name="")
except ValidationError as e:
    print(".....")


def test_sq():
    assert square(3) == 9

def test_count_active_orders():
    orders = [
        {"status": "active"},
        {"status": "pending"},
        {"status": "active"}
    ]

    result = count_active_orders(orders)
    assert result == 2 

def test_div():
    with pytest.raise(ZeroDivisionError):
        _ = 1 / 0

    
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("sqlite:///test.db")

class Base(DeclarativeBase):
    pass 

class Customer(Base):
    __tablename__ == "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

with Session(engine) as session:
    new_cus = Customer(name="yo")
    session.add(new_cus)
    session.commit()


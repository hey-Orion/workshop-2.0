def add_num(a, b):
    return a + b


print(df.head(5))


from pydantic import BaseModel

class Users(BaseModel):
    name: str
    age: int


def is_even(n):
    return n % 2 == 0:


print(df.shape)


from pydantic import BaseModel

class Items(BaseModel):
    item_id: int
    price: float


def get_first_item(items):
    return items[0] if items else None 


result_df = df["customer_id"]


from pydantic import BaseModel

class Config(BaseModel):
    enabled: bool = True


def get_str_length(s):
    return len(s)


result_df = df[df["status"] == "active"]


from pydantic import BaseModel

class UP(BaseModel):
    bio: str | None = None


def to_upper(s):
    return s.upper()


df["price"].mean()


from pydantic import BaseModel

class Tag(BaseModel):
    name: str


import pytest

def test_add():
    assert 1 + 1 == 2 


import requests 

response = requests.get("https://api.example.com/data")
data = response.json()


from sqlalchemy import create_engine 


def test_value_error():
    with pytest.raise(ValueError):
        int("abc")
    

import requests 

response = requests.get("https://api.example.com/data")
if response.status_code == 200:
    data = response.json()


from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")


def test_len():
    assert len("data") == 4


import requests 

params = {"q": "python"}

response = requests.get("https://api.example.com/data", params=params)
data = response.json()


from sqlalchemy import create_engine, Column, Integer, String


@pytest.fixture
def sample_data():
    return [1, 2, 3]


import requests 

headers = {"Authorization": "Bearer my_token"}

response = requests.get("https://api.example.com/data", headers=headers)
data = response.json()


from sqlalchemy.orm import declarative_base 

Base = declarative_base()


class User(Base):
    __tablename__ = "users"


import requests 

response = requests.get("https://api.example.com/data")
response.raise_for_status()
data = response.json()


def test_sample_data(sample_data):
    assert len(sample_data) == 3
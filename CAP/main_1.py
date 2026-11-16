from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    id: int 
    name: str 
    country: Optional[str] = "unknown"

from pydantic import BaseModel, field_validator

class OrderStatus(BaseModel):
    status: str

@field_validator("status")
@classmodel
def validate_status(cls, v: str) -> str:
    v = v.lower()
    if v not in {"pending", "completed"}:
        raise ValueError("status must be 'pending' or 'completed'")
    return v

import requests

def fetch_orders(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

import requests

response = requests.get(
    "https://api.example.com/orders",
    params={"status": "completed"},
    timeout=5,
)
response.raise_for_status()
data = response.json()

import pytest
from pydantic import ValidationError

def test_negative():
    with pytest.raises(ValidationError):
        Order(id:1, amount=-10)
    
import pytest

@pytest.fixture
def sample_orders():
    return [
        {"order_id": 1, "amount": 50.0, "status": "completed"},
        {"order_id": 2, "amount": 25.0, "status": "pending"},
    ]

def test_sample_orders_count(sample_orders):
    assert len(sample_orders) == 2
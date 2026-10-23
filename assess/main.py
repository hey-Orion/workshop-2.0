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


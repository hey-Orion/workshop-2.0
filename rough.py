import requests

def get_paginated_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": 1, "limit": 50}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def send_post_request(url, payload):
    response = requests.post(url, json=payload, timeout=10) 
    response.raise_for_status()
    return response.json()

from typing import Literal
from pydantic import BaseModel, Field

def safe_rq(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except Timeout:
        print('')
        return None

    except HTTPError as e:
        print('') 
        return None 
    
    except RequestException as e:
        print('')
        return None 



from typing import Literal
from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int
    amount: float = Field(gt=0.0)
    status: Literal["p", 'c', 'ca']

from pydantic import ValidationError

def Validate_orders(data: dict):
    try:
        order = Order(**data)
        print("....", order)
        return order 
    except ValidationError as e:
        for error in e.errors:
            filed = "->".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            print("....")

from typing import Literal
from pydantic import BaseModel, Field, field_validator

class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)
    status: Literal["pending", "completed", "cancelled"]

    @field_validator("status", mode="before")
    @classmethod
    def clean_status(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
            if not v:
                raise ValueError("...")
        return v 

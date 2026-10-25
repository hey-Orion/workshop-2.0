# solved
Write a model Order with id as an int, amount as a float that must be greater than 0, and status restricted to "pending", "completed", or "cancelled".

from typing import Literal
from pydantic import BaseModel, Field 

class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)
    status: Literal["pending", "completed", "cancelled"]


Validate a dict against Order. If it’s invalid, catch the ValidationError and print each failing field name and its error message.

from pydantic import ValidationError

def Validate_orders(data: dict):
    try:
        order = Order(**data)
        print(".......", order)
        return order 
    except ValidationError as e:
        for error in e.errors():
            field = "->".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            print(".......")
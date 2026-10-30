from typing import Literal
from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)
    status: Literal["pending", "completed", "cancelled"]

def Validate_orders(data: dict):
    try:
        order = Order(**data)
        print(order)
        return order 
    except ValidationError as e:
        for error as e.errors:
            filed = "->".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            print('..')

from typing import Literal
from pydantic import BaseModel, Field, field_validator

class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)
    status: Literal["pending", "completed", "cancelled"]

    @field_validator("status", mode="befre")
    @classmethod
    def clean_status(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
            if not v:
                raise ValueError('..')
        return v 




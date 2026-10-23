from typing import Optional, Literal, List
from typing_extensions import Self
from datetime import datetime, date 
from pydantic import BaseModel, ConfigDict, EmailStr, ValidationError, Field, field_validator, model_validator

class Order(BaseModel):
    id: int
    amount: float = Field(gt=0)
    status: Literal["pending", "completed", "cancelled"]


def validator(data: dict):
    try:
        order = Order(**data)
        print("valid", order)
        return order 
    except ValidationError as e:
        for error in e.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        print(f"error '{field}': {message}")


@field_validator("status", mode="before")
@classmethod

def clean_status(cls, v: str) -> str:
    if isinstance(v, str):
        v = v.strip().lower()
        if not v:
            raise ValueError("msg")
    return v 


class DateRange(BaseModel):
    start_date: date
    end_date: date
    
    @model_validator(mode="after")
    def date_validator(self) -> Self:
        if self.end_date < self.start_date:
            raise ValueError("msg")
        return self 


class NoteModel(BaseModel):
    note: Optional[str] = None
    tags: List[str] = Field(default_factory=list) what is default_factory and why tags are list
    created_at: datetime = Field(default_factory=datetime.now)


class Customers(BaseModel):
    name: str
    email: EmailStr
    order: List[Order]

data = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "orders": [
        {"id": 1, "amount": 99.99, "status": "pending"},
        {"id": 2, "amount": 15.50, "status": "completed"}
    ]
}

customer = Customers(**data)

first_order_amount = customer.orders[0].amount
print(f"{first_order_amount}")


class APIOrder(BaseModel):
    order_id: int = Field(validation_alias="orderId")
    created_at: datetime = Field(validation_alias="createdAt")

api_data = {"orderId": 34, "createdAt": "2026-10-23T12:00:00"}

order = APIOrder(**api_data)
print(order)

print(order.model_dump()) 


class Order(BaseModel):
    id: int
    amount: float = Field(gt=0)
    status: Literal["pending", "completed", "cancelled"]
    note: Optional[str] = None

raw_json = '{"id": 101, "amount": 45.50, "status": "pending", "note": null}'

order = Order.model_validate_json(raw_json)
print(order)

json_output = order.model_dump_json(exclude_none=True)
print(json_output)


def validate_order_batch(rows: list[dict]):
    valid_models = []
    invalid_rows = []
    
    for index, row in enumerate(rows):
        try:
            order = Order(**data)
            valid_models.append(order)
        except ValidationError as e:
            invalid_rows.append({
                "index": index,
                "data": row,
                "errors": e.errors()
            })
    return valid_models, invalid_rows


class StrictOrder(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True
    )

    id: int 
    amount: float

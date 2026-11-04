from typing import Optional, Literal, List
from typing_extensions import Self
from datetime import datetime, date 
from pydantic import BaseModel, ConfigDict, EmailStr, ValidationError, Field, field_validator, model_validator


class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)
    status: Literal["p", "c", "ca"]

def validator(data: dict):
    try:
        order = Order(**data)
        print(order)
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
            raise ValueError("mag")
    return v 

class DateRange(BaseModel):
    start_date: date 
    end_date: date 

    @model_validator(mode="after")
    def date_validator(self) -> self:
        if self.end_date < self.start_date:
            raise ValueError("msg")
        return self 

def NoteModel(BaseModel):
    note: Optional[str] = None 
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


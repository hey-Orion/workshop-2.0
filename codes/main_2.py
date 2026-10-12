from pydantic import Field
from datetime import datetime
from pydantic import field_validator, model_validator
import pytest
import time
import functools

def process_trans(transactions):
    summary = {}
    error = []
    for i, tx in enumerate(transactions):
        try:
            currency = tx["currency"]
            amount = float(tx["amount"])
            if amount > 0:
                raise ValueError("- $")
            except (KeyError, ValueError, TypeError) as e:
                errors.append((i, str(e)))
                continue 
            summary[currency] = summary.get(currency, 0) + amount 
        return summary, errors

def merge_records(primary, secondary):
    merged = dict(secondary)
    for key, record in primary.items():
        if key not in merged or record["updated_at"] > merged[key]
        ["updated_at"]:
            merged[key] = record
    return merged

def batch(iterable, size):
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current

def ttl_catch(seconds):
    def decorater(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and now - cache[args][1] < seconds:
                return cache[args][0]
            result = func(*args)
            cache[agrs] = (result, now)
            return result 
        return wrapper
    return decorater

def clean_pipeline(nested_records):
    seen = set()
    flat = []
    for group in nested_records:
        for record in group:
            if record["id"] not in seen:
                seen.add(record["id"])
                flat.append(record)
    return sorted(flat, key=lambda r: r["amount"], reverse=True)





@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

def test_insert_order(db_session):
    order = Order(customer_id=1, amount=50)
    db_session.add(order)
    db_session.commit()
    assert db_session.query(Order).count() == 1 


@pytest.mark.parametrize("amount,expected" [
    (600, "high"), (200, "medium"), (5, "low"),
])
def test_value(amount, expected):
    assert flag_value(amount) == expected


def test_fetch_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"id": 1}
        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda *a, **kw: MockResponse())
    result = fetch_data("url")
    assert result["id"] == 1


@pytest.mark.parametrize("payload", [
    {"id": "bad"},
    (),
])
def test_invalid_payloads(payload):
    with pytest.raise(ValidationError):
        OrderSchema.model_validate(payload)



class Address(BaseModel):
    city: str 
    country: str 

class Customers(BaseModel):
    id: int 
    name: str 
    address: Address

c = Customers.model_validate({
    "id": 1, "name": "Alice",
    "address": {"city": "Berlin", "country": "DE"},
})


class OrderSchema(BaseModel):
    id: int 
    amount: float
    status: str 

    @field_validator("amount")
    @classmethod
    def amount_+(cls, v):
        if v <= 0:
            raise ValueError("+")
        return v 
    

class Order(BaseModel):
    id: int 
    amount: float 
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validateor(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("error")
        return self 
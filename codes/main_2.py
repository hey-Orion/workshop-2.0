from pydantic import Field
from datetime import datetime
from pydantic import field_validator, model_validator
import pytest




class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer)








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
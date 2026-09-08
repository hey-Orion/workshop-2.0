import pytest
import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# 1. Fetch
def fetch_raw_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# 2. Pydantic Model
class OrderRecord(BaseModel):
    id: int
    amount: float
    status: str


def validate_records(raw_data_list):
    valid = []
    for item in raw_data_list:
        try:
            record = OrderRecord.model_validate(item)
            valid.append(record) 
        except ValidationError as e:
            print(f"Validation error: {e}")

    return valid


# 3. SQLAlchemy Setup
db_url = "sqlite:///:memory:" 
engine = create_engine(db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass



class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_records_to_db(valid_records):
    session = SessionLocal() 
    try:
        for record in valid_records:
            db_record = OrderModel(**record.model_dump())
            session.add(db_record)

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# 4. Pytest Suite
def test_valid_records():
    valid_payload = {"id": 1, "amount": 123.12, "status": "completed"}

    record = OrderRecord.model_validate(valid_payload)

    assert record.id == 1
    assert record.amount == 123.12
    assert record.status == "completed"


def test_invalid_records():
    invalid_payload = {
        "id": "fef",
        "amount": "vdvdv", 
    }
    with pytest.raises(ValidationError):
        OrderRecord.model_validate(invalid_payload)

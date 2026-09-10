import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import pytest


# --- Models & DB Setup ---
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


# --- Pydantic Schema ---
class ProductSchema(BaseModel):
    id: int
    name: str
    price: float


# --- Pipeline Steps ---
def fetch_data(url: str) -> list[dict]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def validate_records(raw_data: list[dict]) -> list[ProductSchema]:
    valid = []
    for item in raw_data:
        try:
            valid.append(ProductSchema.model_validate(item))
        except ValidationError as e:
            print(f"Skipping invalid record: {e}")
    return valid


def save_records(valid_records: list[ProductSchema]):
    session = SessionLocal()
    try:
        for record in valid_records:
            db_record = Product(**record.model_dump())
            session.add(db_record)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def run_pipeline(url: str):
    raw_data = fetch_data(url)
    validated = validate_records(raw_data)
    save_records(validated)


# --- Tests ---
def test_valid_product_schema():
    payload = {"id": 1, "name": "Keyboard", "price": 120.50}
    record = ProductSchema.model_validate(payload)
    assert record.name == "Keyboard"
    assert record.price == 120.50


def test_invalid_product_schema():
    payload = {"id": "not_a_number", "name": "Keyboard", "price": "not_a_number"}
    with pytest.raises(ValidationError):
        ProductSchema.model_validate(payload)
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"

    id =  Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

def insert_customers(customer_date: dict):
    session = SessionLocal()
    try:
        new_customer = Customer(**customer_date)
        session.add(new_customer)
        session.commit()
    except Exception:
        session.rollback()
    finally:           
        session.close()



# pytest

import pytest


def calculate_discount(amount: float, is_member: bool) -> float:
    if amount > 1000 and is_member:
        return amount * 0.9
    return amount


def test_discount_applied_for_member_over_1000():
    result = calculate_discount(1200, is_member=True)
    assert result == 1080.0
   
def test_no_discount_for_non_member():
    result = calculate_discount(1200, is_member=False)
    assert result == 1200

def test_boundary_amount_1000():
    result = calculate_discount(1000, is_member=True)
    assert result == 1000
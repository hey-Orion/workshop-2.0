from typing import List, Dict, Any, Tuple
import logging
import pytest
from sqlalchemy import func, create_engine
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel, field_validator

logging.basicConfig(level=logger.INFO)

logger = logging.getLogger(__name__)

def simple_etl(source_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    loaded_record = []
    bad_records = []

    for row in source_data:
        try:
            transformed = {
                "id": str(row["id"]),
                "amount": float(row["amount"]),
                "is_active": bool(row["is_active"])
            }
            
            if transformed['amount'] < 0:
                raise ValueError("Amount cannot be negative")

            loaded_record.append(transformed)

        except (KeyError, ValueError, TypeError) as e:

            logged_row = row.copy()
            logged_row['error_reason'] = str(e)
            bad_records.append(logged_row)
            logger.warning(f"ETL Validation Failed for row {row}: {e}")
        
    return loaded_record, bad_records


def get_high_spenders(session: Session) -> list:
    results = (
        session.query(
            Customer.customer_id,
            func.sum(Order.amount).label('total_spend')
        )
        .join(Order, Customer.customer_id == Order.customer_id)
        .group_by(Customer.customer_id)
        .having(func.sum(Order.amount) > 100)
        .all()
    )
    return results 


DB_URL = ""

@pytest.fixture(scope='function')
def db_session():
    engine = create_engine(DB_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class OrderItem(BaseModel):
    item_id: str
    amount: float 

    @field_validator('amount')
    @classmethod
    def valid_amount(cls, value: float) -> float:
        if value < 0:
            raise ValueError('')
        return value 
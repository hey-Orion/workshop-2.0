from pydantic import BaseModel 

class Trade(BaseModel):
    ticker: str
    price: float
    exchange: optional[str] = None




select ticker, avg(price) as avg_p
from data
where price > 0
group by ticker;


select * 
from (
    select *, 
            row_number() over ( 
                partition by ticker
                order by timestamp desc
            ) as rn 
    from trades 
) t 
where rn = 1;


select ticker,
       price
from (
    select ticker,
           price,
           row_number() over (
                partition by ticker
                order by price desc
           ) as rn 
    from trades
) t 
where rn <= 3;


select ticker,
       timestamp,
       count(*) as total
from trades
group by ticker, timestamp
having count(*) > 1;

select ticker,
       timestamp,
       price,
       sum(price) over (
            partition by ticker
            order by timestamp
       ) as running_t 
from trades;


from pydantic import BaseModel

class trade(BaseModel):
    ticker: str 
    price: float



from pydantic import BaseModel
from typing import Optional

class trade(BaseModel):
    ticker: str 
    price: float
    exchange: Optional[str] = None 



from pydantic import BaseModel

class comp(BaseModel):
    name: str
    country: str 

class trade(BaseModel):
    ticker: str 
    price: str 
    company: Company 

what is company 


from pydantic import BaseModel, model_validator

class Trade(BaseModel):
    buy_price: float
    sell_price: float

    @model_validator(mode="after")
    def Validate_p(self):
        if self.sell_price < self,buy_price:
            raise ValueError("sell > buy")
        return self


from pydantic import BaseModel, field_validator

class trade(BaseModel):
    ticker: str 
    price: float

    @field_validator("price")
    def Validate_p(cls, v):
        if v <= 0:
            raise ValueError("posative")
        return v 
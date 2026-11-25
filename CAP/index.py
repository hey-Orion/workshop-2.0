so these are the three layers (cold, helped and code=needed diract code)

from pydantic import BaseModel cold

class Tick(BaseModel):
    ticker: str
    close: float
    volume: int


tick = Tick(ticker="AAPL", close=190.5, volume=1000) helped
print(tick.close)


from pydantic import BaseModel i did the other one with the optional so helped 

class Tick(BaseModel):
    ticker: str
    close: float
    volume: int | None = None


raw = {"ticker": "AAPL", "close": "190.5", "volume": "1000"} code
tick = Tick.model_validate(raw) 

print(type(tick.ticker), type(tick.close), type(tick.volume))


tick_dict = tick.model_dump() code
print(tick_dict)


from pydantic import BaseModel, Field helped

class Tick(BaseModel):
    ticker: str
    close: float = Field(gt=0.0)
    volume: int | None = Field(default=None, ge=0)


from pydantic import ValidationError helped

try:
    Tick.model_validate({"ticker": "AAPL", "close": -5, "volume": 10})
except ValidationError as e:
    print(e)


from typing import Literal helped
from pydantic import BaseModel, Field, ValidationError

class Tick(BaseModel):
    ticker: str 
    close: float = Field(gt=0.0)
    volume: int | None = Field(default=None, ge=0)
    source: Literal["yahoo", "alpha"]

try:
    Tick.model_validate(
        {"ticker": "AAPL", "close": 190.5, "volume": 1000, "source": "bloomberg"}
    )
except ValidationError as e:
    print(e)


from pydantic import BaseModel, field_validator helped

class Tick(BaseModel):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, v: str) -> str:
        return v.strip().upper()


from pydantic import BaseModel, ConfigDict, ValidationError helped

class Tick(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticker: str
    close: float
    volume: int | None = None

try:
    Tick.model_validate(
        {"ticker": "AAPL", "close": 190.5, "volume": 1000, "extra_col": 42}
    )
except ValidationError as exc:
    print(exc)
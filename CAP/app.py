Here is the complete reference sheet for **Questions 1 through 14** using Pydantic v2 conventions and the market-data theme.

### Basics (Q1–Q5)

**1. Define a model `Tick` with `ticker: str`, `close: float`, and `volume: int`.**

```python
from pydantic import BaseModel


class Tick(BaseModel):
    ticker: str
    close: float
    volume: int

```

**2. Create a `Tick` from keyword arguments and print its `close`.**

```python
tick = Tick(ticker="AAPL", close=190.5, volume=1000)
print(tick.close)

```

**3. Make `volume` optional, with a default of `None`.**

```python
from pydantic import BaseModel


class Tick(BaseModel):
    ticker: str
    close: float
    volume: int | None = None

```

**4. Validate `{"ticker": "AAPL", "close": "190.5", "volume": "1000"}` using the v2 method and check field types.**

```python
raw = {"ticker": "AAPL", "close": "190.5", "volume": "1000"}
tick = Tick.model_validate(raw)

print(type(tick.ticker), type(tick.close), type(tick.volume))

```

* **Resulting types:** `ticker` → `str` (`"AAPL"`), `close` → `float` (`190.5`), `volume` → `int` (`1000`) via Pydantic v2's default type coercion.

**5. Convert a `Tick` instance back into a dict.**

```python
tick_dict = tick.model_dump()
print(tick_dict)

```

---

### Medium (Q6–Q10)

**6. Add constraints with `Field`: `close` greater than `0` and `volume` at least `0`.**

```python
from pydantic import BaseModel, Field


class Tick(BaseModel):
    ticker: str
    close: float = Field(gt=0.0)
    volume: int | None = Field(default=None, ge=0)

```

**7. Validate `{"ticker": "AAPL", "close": -5, "volume": 10}` inside `try/except`, catch `ValidationError`, and print errors.**

```python
from pydantic import ValidationError

try:
    Tick.model_validate({"ticker": "AAPL", "close": -5, "volume": 10})
except ValidationError as exc:
    print(exc)

```

**8. Add `source: Literal["yahoo", "alpha"]` and show that an invalid value fails.**

```python
from typing import Literal
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
except ValidationError as exc:
    print(exc)

```

**9. Write a `field_validator` on `ticker` that uppercases it.**

```python
from pydantic import BaseModel, field_validator


class Tick(BaseModel):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, v: str) -> str:
        return v.strip().upper()

```

**10. Reject undefined extra fields using `extra="forbid"`.**

```python
from pydantic import BaseModel, ConfigDict, ValidationError


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

```

---

### Interview Level (Q11–Q14)

**11. Create `Batch` with `batch_id: str` and `records: list[Tick]`, then validate a nested dict into it.**

```python
from pydantic import BaseModel


class Batch(BaseModel):
    batch_id: str
    records: list[Tick]


payload = {
    "batch_id": "batch-2026-11-25",
    "records": [
        {"ticker": "aapl", "close": "190.5", "volume": "1000"},
        {"ticker": "msft", "close": 420.25, "volume": 500},
    ],
}
batch = Batch.model_validate(payload)

```

**12. Parse `'{"ticker":"AAPL","close":190.5,"volume":1000}'` directly into a `Tick`.**

```python
json_str = '{"ticker":"AAPL","close":190.5,"volume":1000}'
tick_from_json = Tick.model_validate_json(json_str)

```

**13. Model with `high` and `low` using a `model_validator` (`after` mode) that raises if `high < low`.**

```python
from typing import Self
from pydantic import BaseModel, Field, model_validator


class PriceRange(BaseModel):
    high: float = Field(gt=0.0)
    low: float = Field(gt=0.0)

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.high < self.low:
            raise ValueError("high must be greater than or equal to low")
        return self

```

**14. Write `validate_records(raw)` returning `(valid_ticks, invalid_items_with_errors)`.**

```python
from typing import Any
from pydantic import ValidationError


def validate_records(
    raw: list[dict[str, Any]],
) -> tuple[list[Tick], list[dict[str, Any]]]:
    valid: list[Tick] = []
    invalid: list[dict[str, Any]] = []

    for item in raw:
        try:
            valid.append(Tick.model_validate(item))
        except ValidationError as exc:
            invalid.append(
                {
                    "item": item,
                    "error": str(exc),
                    "errors": exc.errors(),
                }
            )

    return valid, invalid

```
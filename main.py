from pydantic import BaseModel, Field, ValidationError
from typing import Literal 

class logpayload(BaseModel):
    event_id: int = Field(gt=0)
    environment: Literal["development", "staging", "production"]
    environment_url: str
    metrics: dict[str, float]

raw_data = {
    "event_id": 105,
    "environment": "invalid_env_name",  # Invalid choice!
    "environment_url": "https://api.eu-ops.net",
    "metrics": {"cpu_usage": 84.5, "memory_usage": 61.2}
}

try:
    validated_data = logpayload.model_validate(raw_data)
    print("done")
except ValidationError as e:
    print("error")
    print(e.json())


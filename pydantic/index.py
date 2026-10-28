# solved
Write a model Order with id as an int, amount as a float that must be greater than 0, and status restricted to "pending", "completed", or "cancelled".

from typing import Literal
from pydantic import BaseModel, Field


Validate a dict against Order. If it’s invalid, catch the ValidationError and print each failing field name and its error message.

from pydantic import ValidationError


Add a validator so status is stripped of whitespace and lowercased before validation. Reject it if it’s empty after stripping.

from typing import Literal
from pydantic import BaseModel, Field, field_validator
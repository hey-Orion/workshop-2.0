from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr


import requests

url = "https://api.example.com/users"
response = requests.get(url, params={"status": "active"})
response.raise_for_status()
data = response.json()


import pytest

def test_avb():
    status = True
    assert status is True


import requests

url = "https://api.example.com/users"
response = requests.post(url, json={"name": "jon"})


class address(BaseModel):
    country: str
    pin_code: int
    user: User

user_dict = user.model_dump()


import pytest

def test_zero_div():
    with pytest.raises(ZeroDivisionError):
        val = 1 / 0
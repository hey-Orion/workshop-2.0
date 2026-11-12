def add_num(a, b):
    return a + b


print(df.head(5))


from pydantic import BaseModel

class Users(BaseModel):
    name: str
    age: int


def is_even(n):
    return n % 2 == 0:


print(df.shape)


from pydantic import BaseModel

class Items(BaseModel):
    item_id: int
    price: float


def get_first_item(items):
    return items[0] if items else None 


result_df = df["customer_id"]


from pydantic import BaseModel

class Config(BaseModel):
    enabled: bool = True


def get_str_length(s):
    return len(s)


result_df = df[df["status"] == "active"]


from pydantic import BaseModel

class UP(BaseModel):
    bio: str | None = None


def to_upper(s):
    return s.upper()


df["price"].mean()


from pydantic import BaseModel

class Tag(BaseModel):
    name: str



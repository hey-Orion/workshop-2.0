orders_df[orders_df["status"] == "completed"]["amount"].mean()

orders_df.groupby("customer_id")["amount"].sum()


import pandas as pd

def sum_list(orders):
    return sum(order["amount"] for order in orders)
    i missed the order[] and the last () in this one


from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int 
    amount: float = Field(gt=0.0)


this was my attemp and 

orders_df[orders_df["amount"] > 100]orders_df.get(["order_id", "amount"])
this is the currect one
orders_df.loc[orders_df["amount"] > 100, ["order_id", "amount"]]

orders_df["status"].value_counts() needed hints for this one 


def sort(orders):
    return [order for order in orders if order.get("status") == "completed"]


import pytest

def test_get_total():
    assert get_total([{"amount": 10}, {"amount": 5}]) == 15


orders_df["status"].value_counts()

orders_df.loc[orders_df["amount"] > 200, ["order_id", "order_date"]]

orders_df.groupby("status")["amount"].sum().sort_value(ascending=False)


def get_refunded(orders):
    return [order for order in orders if order.get("status") == "refunded"]

def get_total(orders):
    return sum(order.get("amount", 0) for order in orders)


def test_get_total():
    assert get_total([{"amount": 10}, {"amount": 20}]) == 30
    assert get_total([{"amount": 5}, {"amount": 15}, {"amount": 10}]) == 30


import pandas as pd 
import pytest

orders_df["status"].value_counts()

orders_df.loc[orders_df["amount"] > 200, ["order_id", "order_date"]]

orders_df.groupby("status")["amount"].sum().sort_value(ascending=False)


orders_df["status"].value_counts()

i added the orders_df as an error
orders_df.loc[orders_df["status"] == "completed", here ["order_id", "amount"]]

needed hints for this one 
orders_df.groupby("customer_id")["amount"].mean().sort_values(ascending=False)

this is my first time using nlargest needed code 
orders_df.nlargest(5, "amount")

this is my first time using nunique needed code 
orders_df["customer_id"].nunique()

this is my first time using isna needed code 
orders_df[orders_df["status"].isna()]

needed code for this one 
def get_big_orders(orders, threshold):
    return [order for order in orders if order["amount"] > threshold]

needed code for this one 
def count_by_status(orders):
    counts = {}
    for order in orders:
        status = order["status"]
        counts[status] = counts.get(status, 0) + 1 
    return counts

needed code for this one 
import pytest

@pytest.mark.parametrize(
    "orders, threshold, expected",
    [
        (
            [{"id": 1, "amount": 50}, {"id": 2, "amount": 250}, {"id": 3, "amount": 120}],
            100,
            [{"id": 2, "amount": 250}, {"id": 3, "amount": 120}],
        ),
        (
            [{"id": 1, "amount": 20}, {"id": 2, "amount": 75}],
            100,
            [],
        ),
        (
            [],
            100,
            [],
        ),
    ],
    ids=["some_match", "none_match", "empty_list"],
)
def test_get_big_orders(orders, threshold, expected):
    assert get_big_orders(orders, threshold) == expected

needed code for this one 
def test_get_total_empty():
    assert get_total([]) == 0



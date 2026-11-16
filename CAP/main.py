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

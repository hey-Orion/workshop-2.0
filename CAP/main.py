import pandas as pd 
from pydantic import BaseModel, Field

orders_df[orders_df["status"] == "completed"]["amount"].mean()

orders_df.groupby("customer_id")["amount"].sum()


def get_total(orders): ###
    return sum(order["amount"] for order in orders)


class Order(BaseModel): 
    id: int 
    amount: float = Field(gt=0.0)


orders_df.loc[orders_df["amount"] > 100, ["order_id", "amount"]]

orders_df["status"].value_counts() ###


def get_completed_orders(orders): ###
    return [order for order in orders if order.get("status") == "completed"]


import pytest 

def test_get_total():
    assert get_total([{"amount": 10}, {"amount": 5}]) == 15
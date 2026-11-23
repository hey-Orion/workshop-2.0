orders_df.groupby("customer_id")["order_id"].count()

orders_df.loc[orders_df["amount"] < 50, ["order_id", "status"]]

orders_df.groupby("status")["amount"].sum().sort_values(ascending=True)

orders_df.nsmallest(3, "amount")
orders_df.sort_values("amount", ascending=True).head(3)

orders_df["status"].nunique()

orders_df[orders_df["amount"].notna()]


def get_small_orders(orders, threshold):
    return [order for order in orders if order["amount"] < threshold]

def count_by_customer(orders):
    counts = {}
    for order in orders:
        customer_id = order["customer_id"]
        counts[customer_id] = counts.get(customer_id, 0) + 1 
    return counts 


import pytest

@pytest.mark.parametrize(
    "orders, threshold, expected",
    [
        (
            [{"id": 1, "amount": 25}, {"id": 2, "amount": 150}, {"id": 3, "amount": 40}],
            50,
            [{"id": 1, "amount": 25}, {"id": 3, "amount": 40}],
        ),
        (
            [{"id": 1, "amount": 80}, {"id": 2, "amount": 120}],
            50,
            [],
        ),
        (
            [],
            50,
            [],
        ),
    ],
    ids=["some_match", "none_match", "empty_list"],
)
def test_get_small_orders(orders, threshold, expected):
    assert get_small_orders(orders, threshold) == expected

def test_count_by_customer_empty():
    assert count_by_customer([]) == {}

Qs 


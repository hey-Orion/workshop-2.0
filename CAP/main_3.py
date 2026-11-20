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



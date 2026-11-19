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

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


Qs --
What is a DAG? (two sentences, in your own words).

in ariflow a dag defines a workflow of tasks and dependencise between them specfing with step runs 
before others becouse its acycle there is no loop so it runs in finite order without looping 

What is a primary key? (two sentences, in your own words).

a primary key is a column of unique vaiues to idintify each row of the table
essential for data integrity, deduplication, safe joins, and upserts 

Name two ways to make a load idempotent (two sentences, in your own words).

insert overwriting  
so it overwrites the data rather then dublactiong it 

and upserts using primary key so every row is unique

ETL vs. ELT: which is your own project, and why? (two sentences, in your own words).

i use elt (extract, load, tranform) in my project becouse i wanted to save the cleaned data for future analasys 

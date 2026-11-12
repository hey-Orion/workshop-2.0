# ok this is pandas, python i attemped these myself first then did the bug fixing with ai 
orders_df = (order_id, customer_id, order_date, amount, status)


orders_df[orders_df["status"] == "completed"]["amount"].mean() here i used wrong ()

orders_df.groupby("customer_id")["amount"].sum() here i added & orders_df[] in bettween 


def get_total(orders): needed hints for this one
    return sum(order["amount"] for order in orders)

from pydantic import BaseModel, Field

class Order(BaseModel): 
    id: int 
    amount: float = Field(gt=0.0)


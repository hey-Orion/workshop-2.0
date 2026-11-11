from pydantic import BaseModel

class TransactionRecord(BaseModel):
    transaction_id: str
    customer_id: int 
    amount: float 
    product_category: str 
    is_returned: bool = False


def summarize_sales(df):

    filtered_df = df[df["is_returned"] == False]
    summary = filtered_df.groupby("product_category")["amount"].sum()

    return summary



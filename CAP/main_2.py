import pandas as pd 
import pytest

orders_df["status"].value_counts()

orders_df.loc[orders_df["amount"] > 200, ["order_id", "order_date"]]

orders_df.groupby("status")["amount"].sum().sort_value(ascending=False)


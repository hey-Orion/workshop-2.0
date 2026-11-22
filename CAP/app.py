orders_df.groupby("customer_id")["order_id"].count()

orders_df.loc[orders_df["amount"] < 50, ["order_id", "status"]]

orders_df.loc[orders_df["status"] == "completed", ["order_id", "amount"]]

orders_df.groupby("customer_id")["amount"].mean().sort_values(ascending=False)

counts[status] = counts.get(status, 0) + 1 

assert get_total([]) == 0

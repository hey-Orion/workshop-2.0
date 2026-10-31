def total_c(orders):
    total = 0 
    for order in orders:
        if order["status"] == "completed":
            total += order["amount"]
    return total

avg = orders_df[orders_df["status"] == "completed"]["amount"].mean()


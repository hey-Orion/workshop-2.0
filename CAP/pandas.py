here are the codes many of these codes and functions were new to me
so these are the three layers (cold, helped and code=needed diract code)

orders_df(order_id, customer_id, order_date, amount, status)
customers_df(customer_id, name, country)
prices_df(ticker, trade_date, close)

import pandas as pd helped
orders_df = pd.read_csv("path")
print(orders_dfdf.head(5))

print(orders_df.shape)
print(orders_df.dtypes)


subset_df = orders_df[["amount", "status"]] helped


filter_df = orders_df[(orders_df["amount"] > 100) & (orders_df["status"] == "completed")] helped


status_counts = orders_df["status"].value_counts()
unique_customers = orders_df["customer_id"].nunique() code


orders_df = orders_df.rename(columns={"amount": "order_amount"}) code 
orders_df["amount_with_tax"] = orders_df["order_amount"] * 1.2


grouped_df = orders_df.groupby("customer_id")["amount"].agg(["sum", "mean"]) code


top_5_customers = ( code
    orders_df.groupby("customer_id")["amount"]
    .sum()
    .nlargest(5)   
)


orders_df["amount"] = orders_df["amount"].fillna(0) code
orders_df = orders_df.dropna(subset=["customer_id"])


orders_df["order_date"] = pd.to_datetime(orders_df["order_date"]) code
orders_df["month"] = orders_df["order_date"].dt.month 


orders_df = orders_df.drop_duplicates(subset=["order_id"], keep="last") code


merged_df = orders_df.merge(customers_df, on="customer_id", how="left") code
total_by_country = merged_df.groupby("country")["amount"].sum()


customers_without_orders = customers_df[ code
    ~customers_df["customer_id"].isin(orders_df["customer_id"])
]


no_orders_df = ( code
    customers_df.merge(orders_df, on="customer_id", how="left")
    .loc[lambda d: d["order_id"].isna(), customers_df.columns]
    .drop_duplicates(subset=["customer_id"])
)


prices_df = prices_df.sort_values(["ticker", "trade_date"]) code
prices_df["daily_pct_change"] = prices_df.groupby("ticker")["close"].pct_change()


prices_df = prices_df.sort_values(["ticker", "trade_date"]) code
prices_df["rolling_7_mean"] = (
    prices_df.groupby("ticker")["close"]
    .transform(lambda s: s.rolling(window=7).mean())
)

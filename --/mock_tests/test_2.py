df = df[df["amount"] > 50]

avg_by_category = groupby.("category")['price'].mean()

df['total'] = df['quantity'] * df['price']

cleaned = df.dropna(subset=['email'])

sorted_df = df.sort_values('data', ascending=False)
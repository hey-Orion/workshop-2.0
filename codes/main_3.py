def sum_num(numbers):
    total = 0
    for item in numbers:
        total += item
    return total

def get_evens(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
    return evens 

def clean_str(text):
    return text.strip().upper()

[{"id": 1, "amount": 50}, {"id": 2, "amount": 30}]
def get_total(orders):
    total = 0
    for order in orders:
        total += order['amount']
    return total

def remover(my_list):
    return list(set(my_list))

def div(a, b):
    if b == 0:
        return None
    return a / b 

orders_df.head(5)

orders_df[orders_df['amount'] > 100]

orders_df.groupby('customer_id')['amount'].sum()

merged = orders_df.merge(customers_df, on='customer_id')

orders_df.sort_values('amount', ascending=False)

orders_df.dropna(subset=['customer_id'])

orders_df.isnull().sum()
orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

select c.name, count(o.order_id) as total_orders
from customers c 
join orders o on c.customer_id = o.customer_id
where c.customer_id IN (
    select customer_id
    from where status = 'cancelled'
)
group by c.customer_id, c.name;

select
    order_id,
    customer_id,
    amount,
    (amount / sum(amount) over (partition by customer_id)) * 100 as pct_of_customer_total
from orders;

with first_orders as (
    select
        c.customer_id,
        c.signup_date,
        min(o.order_date) as first_order_date
    from orders o 
    join customers c on c.customer_id = o.customer_id
    group by c.customer_id, c.signup_date
)
select
    avg(first_order_date - signup_date) as avg_day_to_first_order
from first_orders;


order_summary = orders_df.groupby('customer_id').agg(
    total_orders=('order_id','count'),
    total_amount=('amount','sum'),
    avg_amount=('amount','mean'),
).reset_index()

orders_df.loc[orders_df.groupby('customer_id')['order_date'].idxmax()]

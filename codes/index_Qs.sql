now only explain the lines i have marked -
with order_metrics as (
    select
        customer_id,
        order_id,
        order_date,
        amount,
        count(*) over (partition by customer_id) as total_orders,

        avg(amount) over (
            partition by customer_id
            order by order_date, order_id
            rows between unbounded preceding and 1 preceding expain this line what is it doing.
        ) as running_avg_excl_current,

        row_number() over (
            partition by customer_id
            order by order_date desc, order desc expain this line what is it doing.
        ) as rn
    from orders 
)
select 
    customer_id,
    order_id,
    order_date,
    amount as most_recent_amount,
    round(running_avg_excl_current, 2) as running_avg_excl_current,
    case expain this line what is it doing.
        when amount > running_avg_excl_current then 'above'
        when amount < running_avg_excl_current then 'below'
        else 'Equal / No Prior Orders'
    end as comparison_status 
from order_metrics
where total_orders >= 3 
    and rn = 1;



with monthly_rev as (
    select
        customer_id,
        date_trunc('month' order_date) as order_month,
        sum(amount) as rev 
    from orders 
    group by customer_id, date_trunc('month', order_date)
),
mon_calc as (
    select 
        customer_id,
        order_month,
        rev,
        lag(rev, 1) over (partition by customer_id order by order_month) as prev_month_revenue,
        lag( order_month, 1) over (partition by customer_id order by order_month) as prev_month
    from monthly_rev
)
select
    customer_id,
    order_month,
    rev,
    coalesce(prev_month_revenue, 0) as prev_month_revenue,

    case 
        when prev_month is null or prev_month < order_month = interval '1 month' then rev 
        else rev - prev_month_revenue
    end as mon_rev_change
from mon_calc 
order by customer_id, order_month;



with distinct_customer_months as (
    select distinct 
        customer_id,
        date_trunc('month', order_date) as order_month
    from orders 
),
numbered_months as (
    select 
        customer_id,
        order_month,
        row_number() over (partition by customer_id order by order_month) as rn,
        order_month - (row_number() over (partition by customer_id order by order_month) * interval '1 month') as grp
    from distinct_customer_months
)
select distinct
    customer_id
from numbered_months
group by customer_id, grp 
having count(*) >= 3;



select
    p.category,
    sum(oi.quantity * oi.unit_price) as total_rev 
from customers c 
join orders o on c.customer_id = o.customer_id
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = po.product_id
where c.signup_date >= current_date - interval '1 year'
group by p.category
order by total_rev desc;



with customer_total_spend as (
    select
        customer_id,
        sum(amount) as total_spend 
    from orders 
    group by customer_id
),
ranked_customers as (
    select 
        customer_id,
        total_spend,
        ntile(5) over (order by total_spend desc) as spend_quintile 
    from customer_total_spend
)
select
    customer_id,
    total_spend
from ranked_customers
where spend_quintile = 1 
order by total_spend desc;
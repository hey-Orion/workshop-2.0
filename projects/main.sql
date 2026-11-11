select
    product_category,
    sum(amount) as total_sales
from category_summary
order by total_sales desc
limit 1;

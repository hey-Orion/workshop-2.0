DELETE FROM staging_order
WHERE id IN (
    SELECT id FROM (
        SELECT id,
                ROW_NUMBER() OVER (
                    PARTITION BY order_id 
                    ORDER BY ingested_at DESC
                ) as row_num 
        FROM staging_order
    ) t 
    WHERE t.row_num > 1
); 


SELECT
    shipping_country,
    count(id) as total_trans,
    sum(amount_eur) as net_revenue_eur
FROM orders 
WHERE status = 'completed'
GROUP BY shipping_country
ORDER BY net_revenue_eur DESC;


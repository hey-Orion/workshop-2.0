select c.ticker
from compnies c 
left join trade t 
on c.ticker = t.ticker
where t.ticker IS Null; 


select ticker, avg(price) as avg_price
from data
group by ticker;

select ticker, avg(price) as avg_price
from data
group by ticker
where avg(price) > 100;


select * 
from (
    select *,
            row_number() over (
                partition by ticker order by timestamp desc
            ) as rn 
    from data
) t 
where rn = 1; 


SELECT ticker,
       price
FROM (
    SELECT ticker,
           price,
           ROW_NUMBER() OVER (
                PARTITION BY ticker ORDER BY price DESC
           ) AS rn
    FROM trades
) t
WHERE rn <= 3;


select ticker,
       timestamp,
       price,
       sum(price) over (
        partition by ticker order by timestamp 
       ) as ruuning_total
from trade;

CREATE INDEX idx_ticker
ON trades(ticker);


select ticker, timestamp , count(*) as total 

from trade
group by ticker, timestamp
having count(*) > 1;


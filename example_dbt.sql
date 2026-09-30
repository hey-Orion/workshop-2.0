SELECT
    symbol,
    cast(date AS DATE) AS trade_date,
    cast(open AS FLOAT64) AS open_price,
    cast(high AS FLOAT64) AS high_price,
    cast(low AS FLOAT64) AS low_price,
    cast(close AS FLOAT64) AS close_price,
    cast(volume AS INT64) AS volume,
FROM {{ source('raw', 'raw_market_data') }}
where close Is not null


SELECT
    symbol,
    trade_date,
    close_price,
    lag(close_price) over (partition by symbol order by trade_date) as prev_closs_data,
    round(
        (close_price - lag(close_price) over (partition by symbol order by trade_date))
        / lag(close_price) over (partition by symbol order by trade_date) * 100,
        4
    ) as daily_return_pct
FROM {{ ref('stg_market_data') }}


SELECT 
    symbol,
    trade_date,
    daily_return_pct,
    round(
        stddev(daily_return_pct) over (
            partition by symbol
            order by trade_date
            rows between 6 preceding and current row
        ), 4
    ) as vol
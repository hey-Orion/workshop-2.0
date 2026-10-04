select 
    symbol,
    cast(date as DATE) as trade_date,
    CAST(date AS DATE) AS trade_date,
    CAST(open AS FLOAT64) AS open_price,
    CAST(high AS FLOAT64) AS high_price,
    CAST(low AS FLOAT64) AS low_price,
    CAST(close AS FLOAT64) AS close_price,
    CAST(volume AS INT64) AS volume
from {{ source('row', 'raw_market_data') }}
where close is not null 

select
    symbol,
    trade_date,
    close_price,
    lag(close_price) over (PARTITION by symbol order by trade_date) as prev_close_price,
    ROUND(
        (close_price - lag(close_price) over (PARTITION by symbol order by trade_date))
        / lag(close_price) over (PARTITION by symbol order by trade_date) * 100,
        4
    ) as daily_return_pct
from {{ ref('stg_market_data') }}

with moving_averages as (
    select 
        symbol,
        trade_date,
        close_price
        avg(close_price) over (
            PARTITION by symbol
            order by trade_date
            raw BETWEEN 6 PRECEDING and CURRENT ROW
        ) as ma_7d,
        avg(close_price) over (
            PARTITION by symbol
            order by trade_date
            rows BETWEEN 29 PRECEDING and CURRENT row 
        ) as ma_30d
    from {{ ref('stg_maket_data') }}
),

with_signal as (
    select
        *,
        CASE
            WHEN ma_7d > ma_30d THEN 'BULLISH'
            WHEN ma_7d < ma_30d THEN 'BEARISH'
            ELSE 'NEUTRAL'
        END AS trend_signal,
        LAG(CASE WHEN ma_7d > ma_30d THEN 'BULLISH' ELSE 'BEARISH' END)
            OVER (PARTITION BY symbol ORDER BY trade_date) AS prev_trend_signal
    FROM moving_averages
)

SELECT
    symbol,
    trade_date,
    close_price,
    ROUND(ma_7d, 4) AS ma_7d,
    ROUND(ma_30d, 4) AS ma_30d,
    trend_signal,
    CASE
        WHEN trend_signal != prev_trend_signal THEN TRUE
        ELSE FALSE
    END AS is_crossover_point
FROM with_signal

SELECT
    symbol,
    trade_date,
    daily_return_pct,
    ROUND(
        STDDEV(daily_return_pct) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 4
    ) AS volatility_7d,
    ROUND(
        STDDEV(daily_return_pct) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 4
    ) AS volatility_30d
FROM {{ ref('daily_returns') }}
WHERE daily_return_pct IS NOT NULL

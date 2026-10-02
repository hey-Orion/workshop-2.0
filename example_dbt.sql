SELECT
symbol,
    CAST(date AS DATE) AS trade_date,
    CAST(open AS FLOAT64) AS open_price,
    CAST(high AS FLOAT64) AS high_price,
    CAST(low AS FLOAT64) AS low_price,
    CAST(close AS FLOAT64) AS close_price,
    CAST(volume AS INT64) AS volume
from {{ source('raw', 'raw_market_data') }}
where close is not null

SELECT 
    symbol,
    trade_date,
    close_price,
    LAG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date) AS prev_close_price,
    ROUND(
        (close_price - LAG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date))
        / LAG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date) * 100,
        4
    ) AS daily_return_pct
FROM {{ ref('stg_market_data') }}

WITH moving_averages AS (
    SELECT
        symbol,
        trade_date,
        close_price,
        AVG(close_price) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS ma_7d,
        AVG(close_price) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS ma_30d
    FROM {{ ref('stg_market_data') }}
),

with_signal AS (
    SELECT
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
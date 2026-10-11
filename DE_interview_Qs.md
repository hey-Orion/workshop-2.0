1. Write a SQL query to find each customer's most recent order and whether it's above or below their running average spend (excluding the current order), for customers with 3+ orders.

2. Given an `orders` table, write a query showing month-over-month revenue change per customer, including months with no prior-month orders.

3. Write a query to find customers who placed orders in 3 or more consecutive months.

4. Given `orders`, `order_items`, and `products` tables, write a query for total revenue by product category, limited to customers who signed up in the last 12 months.

5. Write a query to find the top 20% of customers by total spend using a percentile/ranking function.

6. Write a Python function that reads a list of transaction dicts, sums amounts per currency, and separately collects records with missing or invalid fields instead of crashing.

7. Write a Python generator that yields fixed-size batches from any iterable, for chunking API calls.

8. Write a Python decorator that caches a function's result for N seconds, then re-computes on expiry.

9. Write a Python function that merges two dicts of records keyed by ID, keeping whichever record has the more recent `updated_at`.

10. Given a raw pandas DataFrame of orders with duplicate rows and messy status strings, clean it, deduplicate keeping the latest row per order ID, and flag orders that deviate more than 50% from that customer's rolling 3-order average.

11. Given `orders` and `order_items` DataFrames, merge them and compute total revenue per order without double-counting from the join.

12. Using pandas, compute each customer's tenure in days (first order to most recent) and their order frequency, per customer group.

13. Given a DataFrame indexed by date, compute daily revenue and a 7-day rolling average.

14. Write a function that fetches all pages of a paginated API until there's no next-page link, handling timeouts.

15. Write a function that fetches records for a list of IDs from an API, where one failed ID shouldn't stop the rest of the batch.

16. Design a simple ETL function: extract rows from a source (list of dicts), transform by validating/casting types, and load into a destination list — with bad rows logged, not dropped silently.

17. Write a SQLAlchemy query that returns each customer's total spend, filtered to only customers whose total exceeds €100.

18. Write a pytest fixture that sets up and tears down a database session for use across multiple tests.

19. Write a Pydantic model with a custom validator that rejects a negative `amount` field.

20. Given a large table of time-series sensor/metric readings, write a SQL query to detect gaps — timestamps where no reading was recorded for more than 1 hour.

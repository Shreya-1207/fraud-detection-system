-- Query 1: fraud vs normal summary
SELECT Class,
       COUNT(*) AS n,
       ROUND(AVG(Amount), 2) AS avg_amount,
       ROUND(MAX(Amount), 2) AS max_amount
FROM transactions
GROUP BY Class;

-- Query 2: fraud rate by hour (relative to the start of the data)
SELECT CAST(Time / 3600 AS INTEGER) % 24 AS hour_of_day,
       COUNT(*) AS txns,
       SUM(Class) AS frauds,
       ROUND(100.0 * SUM(Class) / COUNT(*), 3) AS fraud_pct
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- Query 3: feature table (this one becomes your model input)
SELECT rowid AS txn_id,
       Time,
       Amount,
       Class,
       CAST(Time / 3600 AS INTEGER) % 24 AS hour_of_day,
       COUNT(*) OVER (ORDER BY Time
                      RANGE BETWEEN 60 PRECEDING AND 1 PRECEDING) AS txns_last_60s,
       AVG(Amount) OVER (ORDER BY Time
                         ROWS BETWEEN 100 PRECEDING AND 1 PRECEDING) AS avg_amount_last_100
FROM transactions;
-- Churn by tenure bucket.
-- Observation end is 2023-12-31 (end of the usage year).

WITH tenure AS (
    SELECT
        c.customer_id,
        ch.churn,
        ((DATE '2023-12-31' - c.signup_date) / 30) AS tenure_months
    FROM customers c
    INNER JOIN churn_labels ch ON ch.customer_id = c.customer_id
)
SELECT
    CASE
        WHEN tenure_months < 12 THEN '00-11 months'
        WHEN tenure_months < 24 THEN '12-23 months'
        WHEN tenure_months < 36 THEN '24-35 months'
        WHEN tenure_months < 48 THEN '36-47 months'
        ELSE '48+ months'
    END AS tenure_bucket,
    COUNT(*) AS customers,
    SUM(churn)::INTEGER AS churners,
    ROUND(100.0 * SUM(churn) / COUNT(*), 2) AS churn_rate_pct
FROM tenure
GROUP BY 1
ORDER BY 1;

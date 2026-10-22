-- Churn rate by contract type.

SELECT
    c.contract_type,
    COUNT(*) AS customers,
    SUM(ch.churn)::INTEGER AS churners,
    ROUND(100.0 * SUM(ch.churn) / COUNT(*), 2) AS churn_rate_pct
FROM core.customers c
INNER JOIN core.churn_labels ch ON ch.customer_id = c.customer_id
GROUP BY c.contract_type
ORDER BY churn_rate_pct DESC;

-- Complaints by contract and region.
-- ML segments are not available yet; these are business groupings.

SELECT
    c.contract_type,
    c.region,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(AVG(u.complaints)::NUMERIC, 2) AS avg_monthly_complaints,
    SUM(u.complaints) AS total_complaints
FROM customers c
INNER JOIN customer_usage u ON u.customer_id = c.customer_id
GROUP BY c.contract_type, c.region
ORDER BY avg_monthly_complaints DESC;

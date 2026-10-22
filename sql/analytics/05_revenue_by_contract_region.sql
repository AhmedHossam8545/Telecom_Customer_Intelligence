-- Monthly revenue proxy by contract and region (sum of monthly_charges).

SELECT
    c.contract_type,
    c.region,
    COUNT(*) AS customers,
    ROUND(SUM(c.monthly_charges)::NUMERIC, 2) AS monthly_revenue,
    ROUND(AVG(c.monthly_charges)::NUMERIC, 2) AS avg_monthly_charges
FROM customers c
GROUP BY c.contract_type, c.region
ORDER BY monthly_revenue DESC;

-- Row counts and referential checks after loading into core tables.

SELECT 'customers' AS check_name, COUNT(*)::BIGINT AS value
FROM core.customers
UNION ALL
SELECT 'customer_usage', COUNT(*)
FROM core.customer_usage
UNION ALL
SELECT 'churn_labels', COUNT(*)
FROM core.churn_labels
UNION ALL
SELECT 'customers_missing_usage', COUNT(*)
FROM core.customers c
LEFT JOIN core.customer_usage u ON u.customer_id = c.customer_id
WHERE u.customer_id IS NULL
UNION ALL
SELECT 'customers_missing_churn', COUNT(*)
FROM core.customers c
LEFT JOIN core.churn_labels ch ON ch.customer_id = c.customer_id
WHERE ch.customer_id IS NULL;

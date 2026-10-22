-- Average monthly usage by churn status.

SELECT
    ch.churn,
    ROUND(AVG(u.call_minutes), 2) AS avg_call_minutes,
    ROUND(AVG(u.data_usage_gb), 2) AS avg_data_gb,
    ROUND(AVG(u.sms_count), 2) AS avg_sms,
    ROUND(AVG(u.complaints), 2) AS avg_complaints,
    COUNT(DISTINCT u.customer_id) AS customers,
    COUNT(*) AS usage_rows
FROM customer_usage u
INNER JOIN churn_labels ch ON ch.customer_id = u.customer_id
GROUP BY ch.churn
ORDER BY ch.churn;

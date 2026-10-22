-- -- High-value / high-risk customers using a transparent proxy.
-- -- Value: monthly_charges in the top quartile.
-- -- Risk: churned, or above-average complaint rate.
-- -- This is not a CLV model and not a predicted churn score

-- WITH usage_agg AS (
--     SELECT
--         customer_id,
--         AVG(complaints)::NUMERIC AS avg_complaints,
--         AVG(data_usage_gb)::NUMERIC AS avg_data_gb
--     FROM customer_usage
--     GROUP BY customer_id
-- ),
-- thresholds AS (
--     SELECT
--         PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_charges) AS charges_p75
--     FROM customers
-- ),
-- complaint_threshold AS (
--     SELECT AVG(avg_complaints) AS complaints_avg
--     FROM usage_agg
-- )
-- SELECT
--     c.customer_id,
--     c.contract_type,
--     c.region,
--     c.monthly_charges,
--     ((DATE '2023-12-31' - c.signup_date) / 30) AS tenure_months,
--     ROUND(u.avg_complaints, 2) AS avg_complaints,
--     ROUND(u.avg_data_gb, 2) AS avg_data_gb,
--     ch.churn,
--     CASE
--         WHEN c.monthly_charges >= t.charges_p75
--              AND (ch.churn = 1 OR u.avg_complaints > ct.complaints_avg)
--             THEN 'Critical'
--         WHEN c.monthly_charges >= t.charges_p75
--             THEN 'Maintain'
--         WHEN ch.churn = 1 OR u.avg_complaints > ct.complaints_avg
--             THEN 'Standard'
--         ELSE 'Low priority'
--     END AS retention_priority
-- FROM customers c
-- INNER JOIN churn_labels ch ON ch.customer_id = c.customer_id
-- INNER JOIN usage_agg u ON u.customer_id = c.customer_id
-- CROSS JOIN thresholds t
-- CROSS JOIN complaint_threshold ct
-- ORDER BY c.monthly_charges DESC, u.avg_complaints DESC;


-- -- High-value / high-risk customers using a transparent proxy.
-- -- Value: monthly_charges in the top quartile.
-- -- Risk: churned, or above-average complaint rate.
-- --Ordered by retention priority, then monthly_charges, then avg_complaints
WITH usage_agg AS (
    SELECT
        customer_id,
        AVG(complaints)::NUMERIC AS avg_complaints,
        AVG(data_usage_gb)::NUMERIC AS avg_data_gb
    FROM customer_usage
    GROUP BY customer_id
),
thresholds AS (
    SELECT
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_charges) AS charges_p75
    FROM customers
),
complaint_threshold AS (
    SELECT AVG(avg_complaints) AS complaints_avg
    FROM usage_agg
),
scored_customers AS (
    SELECT
        c.customer_id,
        c.contract_type,
        c.region,
        c.monthly_charges,
        ((DATE '2023-12-31' - c.signup_date) / 30) AS tenure_months,
        ROUND(u.avg_complaints, 2) AS avg_complaints,
        ROUND(u.avg_data_gb, 2) AS avg_data_gb,
        ch.churn,
        CASE
            WHEN c.monthly_charges >= t.charges_p75
                 AND (ch.churn = 1 OR u.avg_complaints > ct.complaints_avg)
                THEN 'Critical'
            WHEN c.monthly_charges >= t.charges_p75
                THEN 'Maintain'
            WHEN ch.churn = 1 OR u.avg_complaints > ct.complaints_avg
                THEN 'Standard'
            ELSE 'Low priority'
        END AS retention_priority
    FROM customers c
    INNER JOIN churn_labels ch ON ch.customer_id = c.customer_id
    INNER JOIN usage_agg u ON u.customer_id = c.customer_id
    CROSS JOIN thresholds t
    CROSS JOIN complaint_threshold ct
)
SELECT *
FROM scored_customers
ORDER BY 
    CASE retention_priority
        WHEN 'Critical' THEN 1
        WHEN 'Maintain' THEN 2
        WHEN 'Standard' THEN 3
        ELSE 4
    END ASC,
    monthly_charges DESC,
    avg_complaints DESC;
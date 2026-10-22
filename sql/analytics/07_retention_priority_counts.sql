-- Counts by retention-priority tier (paste this into the notebook, not all 10k rows).

WITH usage_agg AS (
    SELECT
        customer_id,
        AVG(complaints)::NUMERIC AS avg_complaints
    FROM core.customer_usage
    GROUP BY customer_id
),
thresholds AS (
    SELECT
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_charges) AS charges_p75
    FROM core.customers
),
complaint_threshold AS (
    SELECT AVG(avg_complaints) AS complaints_avg
    FROM usage_agg
),
scored AS (
    SELECT
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
    FROM core.customers c
    INNER JOIN core.churn_labels ch ON ch.customer_id = c.customer_id
    INNER JOIN usage_agg u ON u.customer_id = c.customer_id
    CROSS JOIN thresholds t
    CROSS JOIN complaint_threshold ct
)
SELECT
    retention_priority,
    COUNT(*) AS customers
FROM scored
GROUP BY retention_priority
ORDER BY
    CASE retention_priority
        WHEN 'Critical' THEN 1
        WHEN 'Maintain' THEN 2
        WHEN 'Standard' THEN 3
        ELSE 4
    END;

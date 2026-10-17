WITH customer_metrics AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders,
        AVG(DATEDIFF(day, purchase_timestamp, delivered_customer_date)) AS avg_delivery_time
    FROM {{ ref('order_enriched_model') }} 
    GROUP BY customer_unique_id
)
SELECT
    customer_unique_id,
    total_orders,
    avg_delivery_time,
    CASE
        WHEN total_orders > 1 THEN 1
        ELSE 0
    END AS repeat_customer_flag
FROM customer_metrics
SELECT 
    city,
    COUNT(order_id) AS total_orders,
    --delivered orders
    COUNT(CASE WHEN status = 'DELIVERED' THEN order_id END) AS delivered_orders,
    --average delivery time
    AVG(DATEDIFF(day, purchase_timestamp, delivered_customer_date)) AS avg_delivery_time
FROM {{ ref('order_enriched_model') }}
GROUP BY city
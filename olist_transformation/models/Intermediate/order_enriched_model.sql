WITH o AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
),
c AS (
    SELECT *
    FROM {{ ref('stg_customers') }}
)
/* 1. Join the orders and customers tables on customer_id. This block above is saying run this query and temporarily call the result "Order" and "Customer" */
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.status,
    c.city,
    o.purchase_timestamp,
    o.delivered_customer_date
FROM o
LEFT JOIN c ON o.customer_id = c.customer_id

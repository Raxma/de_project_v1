/*Import CTE: Bring in the raw data from the source table */
WITH raw_orders AS (
    SELECT *
    FROM {{ source('olist_raw', 'OLIST_ORDERS') }}
),
/*Logical CTE: Apply necessary transformations to clean and standardize the data */
cleaned_orders AS (
    SELECT
        ORDER_ID AS order_id,
        CUSTOMER_ID AS customer_id,
        UPPER(order_status) AS status, -- Standardize to uppercase
        order_purchase_timestamp AS purchase_timestamp,
        order_approved_at AS approved_at,
        order_delivered_carrier_date AS delivered_carrier_date,
        order_delivered_customer_date AS delivered_customer_date,
        order_estimated_delivery_date AS estimated_delivery_date
    FROM raw_orders
)/*Final CTE: Select the cleaned data for the final output */
SELECT * FROM cleaned_orders

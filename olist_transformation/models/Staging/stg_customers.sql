/* 1. Import CTE: Bring in the raw data from the source table. CTE is common table expression */
WITH raw_customers AS (
    SELECT *
    FROM {{ source('olist_raw', 'OLIST_CUSTOMERS') }}
),

/* 2. Logical CTE: Apply necessary transformations to clean and standardize the data */
cleaned_customers AS (
    SELECT
        CUSTOMER_ID AS customer_id,
        UPPER(customer_unique_id) AS customer_unique_id, -- Standardize to uppercase
        TRIM(customer_zip_code_prefix) AS zip_code, -- Remove leading/trailing spaces
        TRIM(customer_city) AS city, -- Remove leading/trailing spaces
        TRIM(customer_state) AS state -- Remove leading/trailing spaces
    FROM raw_customers /*raw_customers is the name of first block therefore my second block needs to reach back and pull from that name instead of reaching all the way back to the databse it will reach back to the block I just defined above it */
)
/* 3. Final CTE: Select the cleaned data for the final output */
SELECT *
FROM cleaned_customers
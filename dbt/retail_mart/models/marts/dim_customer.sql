{{ config(materialized='table', schema='dims') }}

select
    md5(customer_id::text) as customer_key,   -- surrogate key
    customer_id,
    country
from {{ source('core', 'customers') }}
where customer_id is not null

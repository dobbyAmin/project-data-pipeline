{{ config(materialized='table') }}

select distinct
    "CustomerID" as customer_id,
    "Country" as country
from {{ source('staging', 'raw_data') }}
where "CustomerID" is not null

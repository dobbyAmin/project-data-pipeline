{{ config(materialized='table') }}

select distinct
    "StockCode" as stock_code,
    "Description" as description,
    "UnitPrice" as unit_price
from {{ source('staging', 'raw_data') }}
where "StockCode" is not null

{{ config(materialized='table', schema='dims') }}

select
    md5(stock_code::text) as stock_key,   -- surrogate key
    stock_code,
    description,
    unit_price
from {{ source('core', 'stock') }}
where stock_code is not null

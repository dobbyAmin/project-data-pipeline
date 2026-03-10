{{ config(materialized='table', schema='sales') }}

with base as (
    select
        s.invoice_no,
        s.stock_code,
        s.customer_id,
        s.quantity,
        s.invoice_date
    from {{ source('core', 'sales') }} as s
    where s.invoice_no  is not null
      and s.stock_code  is not null
      and s.customer_id is not null
      and s.quantity    is not null
      and s.quantity > 0
)
select
    b.invoice_no,
    d.date_key   as invoice_date_key,
    dc.customer_key,
    ds.stock_key,
    b.quantity
from base b
-- Join on surrogate keys (md5 hashed natural keys)
join {{ ref('dim_date') }} d on b.invoice_date = d.full_date
join {{ ref('dim_customer') }} dc on b.customer_id = dc.customer_id
join {{ ref('dim_stock') }} ds on b.stock_code = ds.stock_code

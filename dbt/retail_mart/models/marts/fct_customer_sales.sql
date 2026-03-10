{{ config(materialized='table', schema='customer') }}

with customer_sales as (
    select
        s.customer_id,
        min(s.invoice_date) as first_invoice_date,
        max(s.invoice_date) as last_invoice_date,
        count(distinct s.invoice_no) as total_invoices,
        sum(s.quantity) as total_quantity
    from {{ source('core', 'sales') }} as s
    group by s.customer_id
)
select
    dc.customer_key,
    d1.date_key as first_invoice_date_key,
    d2.date_key as last_invoice_date_key,
    cs.total_invoices,
    cs.total_quantity
from customer_sales cs
join {{ ref('dim_customer') }} dc on cs.customer_id = dc.customer_id
left join {{ ref('dim_date') }} d1 on cs.first_invoice_date = d1.full_date
left join {{ ref('dim_date') }} d2 on cs.last_invoice_date = d2.full_date

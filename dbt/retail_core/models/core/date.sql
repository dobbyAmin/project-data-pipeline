{{ config(materialized='table') }}

with source_dates as (
    select distinct
        to_timestamp("InvoiceDate", 'DD/MM/YYYY HH24:MI')::date as invoice_date
    from {{ source('staging', 'raw_data') }}
    where "InvoiceDate" is not null
)

select
    invoice_date as date_day,
    extract(day from invoice_date)::int as day,
    extract(month from invoice_date)::int as month,
    extract(year from invoice_date)::int as year
from source_dates
order by date_day

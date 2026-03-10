{{ config(materialized='table') }}

select distinct
    r."InvoiceNo" as invoice_no,
    r."StockCode" as stock_code,
    r."CustomerID" as customer_id,
    r."Quantity" as quantity,
    to_timestamp(r."InvoiceDate", 'DD/MM/YYYY HH24:MI')::date as invoice_date
from {{ source('staging', 'raw_data') }} as r
join {{ ref('stock') }} as st
  on st.stock_code = r."StockCode"
where r."InvoiceNo" is not null

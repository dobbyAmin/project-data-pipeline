{{ config(materialized='table', schema='dims') }}

with dates as (
    -- หา min/max date จากทั้ง orders และ payments
    select
        min(date_day) as min_date,
        max(date_day) as max_date
    from {{ source('core', 'date') }}
),
date_series as (
    select
        generate_series(
            (select min_date from dates),
            (select max_date from dates),
            interval '1 day'
        )::date as date_day
)
select
    md5(date_day::text) as date_key,  -- surrogate key
    date_day as full_date,
    extract(day from date_day) as day,
    extract(month from date_day) as month,
    to_char(date_day, 'Month') as month_name,
    extract(year from date_day) as year,
    extract(quarter from date_day) as quarter,
    extract(dow from date_day) as day_of_week,
    case when extract(dow from date_day) in (6,0) then true else false end as is_weekend
from date_series

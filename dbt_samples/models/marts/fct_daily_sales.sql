{{
    config(
        materialized='incremental',
        unique_key='order_date',
        on_schema_change='append_new_columns'
    )
}}

with enriched as (
    select
    *
    from 
    --analytics.int_order_items_enriched 
    {{ ref('int_order_items_enriched') }}
)

select
order_date,
count(distinct order_id) as order_count,
sum(line_revenue) as total_revenue,
sum(line_margin) as total_margin
from
enriched 


{% if is_incremental() %}
-- Only runs on incremental refreshes: keep rows dated after the newest date we
-- have already loaded. 'this' refers to the existing table being added to.
where order_date > (select coalesce(max(order_date), '1900-01-01') from {{ this }})
{% endif %}

group by
order_date
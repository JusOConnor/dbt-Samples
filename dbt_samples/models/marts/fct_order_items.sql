{{
    config(
        materialized='incremental',
        unique_key='order_item_id',
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
    {{ dbt_utils.generate_surrogate_key(['order_item_id']) }} as order_item_sk,
    order_item_id,
    order_id,
    customer_id,
    product_id,
    order_date,
    status,
    category,
    subcategory,
    quantity,
    unit_price,
    discount,
    line_revenue,
    line_cost,
    line_margin
from enriched

{% if is_incremental() %}
where order_date > (select coalesce(max(order_date), '1900-01-01') from {{ this }})
{% endif %}

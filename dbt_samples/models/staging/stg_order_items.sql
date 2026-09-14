with source as (
    select
    *
    from
    --analytics.raw_order_items
    {{ source('foodservice', 'raw_order_items') }}
)

select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount
from source

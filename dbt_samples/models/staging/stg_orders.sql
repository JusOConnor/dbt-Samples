with source as (
    select
    *
    from
    --analytics.raw_orders
    {{ source('foodservice', 'raw_orders') }}
)

select
    order_id,
    customer_id,
    cast(order_date as date) as order_date,
    lower(status) as status,
    channel
from source

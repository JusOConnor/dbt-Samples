with items as (
    select
    *
    from
    --analytics.fct_order_items 
    {{ ref('fct_order_items') }}
)

select
    order_id,
    customer_id,
    order_date,
    status,
    count(*) as line_count,
    sum(quantity) as total_units,
    sum(line_revenue) as order_revenue,
    sum(line_cost) as order_cost,
    sum(line_margin) as order_margin
from items
group by order_id, customer_id, order_date, status

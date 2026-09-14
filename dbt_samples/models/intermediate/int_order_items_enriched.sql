with items as (
    select * 
    from 
    --analytics.stg_order_items 
    {{ ref('stg_order_items') }}
),

orders as (
    select 
    * 
    from 
    --analytics.stg_orders 
    {{ ref('stg_orders') }}
),

products as (
    select
    *
    from
    --analytics.stg_products 
    {{ ref('stg_products') }}
),

joined as (
    select
        items.order_item_id,
        items.order_id,
        orders.customer_id,
        orders.order_date,
        orders.status,
        items.product_id,
        products.category,
        products.subcategory,
        items.quantity,
        items.unit_price,
        items.discount,
        -- Revenue is quantity times price, less any discount.
        round((items.quantity * items.unit_price * (1 - items.discount))::numeric, 2) as line_revenue,
        -- Cost uses the product unit cost. Missing costs are treated as zero so a
        -- gap in the catalog never breaks the calculation.
        round((items.quantity * coalesce(products.unit_cost, 0))::numeric, 2) as line_cost
    from items
    inner join orders on items.order_id = orders.order_id
    inner join products on items.product_id = products.product_id
)

select
    *,
    round((line_revenue - line_cost)::numeric, 2) as line_margin
from joined

with customers as (
    select
    *
    from
    --analytics.dim_customers
    {{ ref('dim_customers') }}
),

orders as (
    select
    *
    from
    --analytics.fct_orders
    {{ ref('fct_orders') }}
)

select
    customers.customer_id,
    customers.customer_name,
    customers.segment,
    count(distinct orders.order_id) as lifetime_orders,
    coalesce(sum(orders.order_revenue), 0) as lifetime_revenue,
    coalesce(sum(orders.order_margin), 0) as lifetime_margin,
    max(orders.order_date) as most_recent_order_date
from customers
left join orders on customers.customer_id = orders.customer_id
group by customers.customer_id, customers.customer_name, customers.segment

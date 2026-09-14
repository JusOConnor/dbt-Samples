with orders as (
select
customer_id,
order_id,
sum(line_revenue) as total_revenue,
sum(line_margin) as total_margin
from 
--analytics.fct_order_items
{{ ref('fct_order_items') }}
group by
customer_id,
order_id
),

customers as (
select channel, customer_id, order_id
from
--analytics.stg_orders
{{ ref('stg_orders') }}
)

select
c.channel as channel,
count(distinct o.order_id  ) as order_count,
sum(o.total_revenue ) as total_revenue,
sum(o.total_margin ) as total_margin
from
customers as c
inner join orders as o
on o.customer_id = c.customer_id and o.order_id = c.order_id 
group by
c.channel 
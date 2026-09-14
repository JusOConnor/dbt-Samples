with orderitems as (
select
order_id
from
--analytics.fct_order_items
{{ ref('fct_order_items')}}
where
product_id is not null
)
select
o.order_id
from
--analytics.fct_orders o
{{ ref('fct_orders')}} as o
left join orderitems as oi
on o.order_id = oi.order_id 
where
oi.order_id is null
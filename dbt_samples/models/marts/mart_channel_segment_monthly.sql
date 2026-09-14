with orders as (
	select
	date_trunc('month', order_date)::date as month_start,
	customer_id,
	order_id,
	line_revenue,
	line_margin
	from
	--analytics.fct_order_items 
    {{ ref('fct_order_items') }}
	),
orderss as (
	select
	date_trunc('month', order_date)::date as month_start,
	customer_id,
	order_id,
	sum(line_revenue) as total_revenue,
	sum(line_margin) as total_margin
	from
	-- analytics.fct_order_items 
    {{ ref('fct_order_items') }}
	group by 
	date_trunc('month', order_date)::date,
	customer_id,
	order_id
	),
customers as (
	select
	customer_id,
	segment
	from
	-- analytics.stg_customers
    {{ ref('stg_customers') }}
	),
channels as (
select channel, customer_id, order_id
from
--{{ ref('stg_orders') }}
analytics.stg_orders
)
select
ch.channel,
c.segment,
o.month_start,
sum(o.line_revenue) as total_revenue,
sum(o.line_margin) as total_margin
from 
orders as o
left join customers c
on o.customer_id = c.customer_id
left join channels ch
on o.customer_id = ch.customer_id and o.order_id = ch.order_id
group by
ch.channel,
c.segment,
o.month_start

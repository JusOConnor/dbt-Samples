with orders as (
	select
	customer_id,
	line_revenue,
	line_margin
	from
	-- analytics.fct_order_items
    {{ ref('fct_order_items') }}
),
customers as (
	select
	customer_id,
	state,
	segment
	from
	-- analytics.stg_customers
    {{ ref('stg_customers') }}
),
region as (
	select
	state,
	region
	from
	-- analytics.state_region_map
    {{ ref('state_region_map') }}
)
select
c.segment,
r.region,
count(distinct c.customer_id) as customer_count,
sum(o.line_revenue) as total_revenue,
sum(o.line_margin) as total_margin
from 
orders as o
inner join customers as c
on o.customer_id  = c.customer_id 
left join region as r
on c.state = r.state 
group by
c.segment,
r.region
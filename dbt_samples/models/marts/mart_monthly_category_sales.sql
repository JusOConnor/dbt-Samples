with orders as (
select
date_trunc('month', order_date)::date as month_start,
category ,
line_revenue ,
line_margin 
from
--analytics.fct_order_items
{{ ref('fct_order_items') }}
)

select
month_start,
category,
sum(line_revenue) as total_revenue,
sum(line_margin) as total_margin,
{{ margin_pct('sum(line_margin)', 'sum(line_revenue)') }} as margin_pct 
from orders
group by
month_start,
category
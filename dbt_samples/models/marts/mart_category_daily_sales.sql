with items as (
    select
    *
    from
    --analytics.fct_order_items
    {{ ref('fct_order_items') }}
)

select
    order_date,
    category,
    count(distinct order_id) as order_count,
    sum(quantity) as total_units,
    sum(line_revenue) as total_revenue,
    sum(line_margin) as total_margin,
    -- Margin percent, computed by the macro so the logic lives in one place.
    {{ margin_pct('sum(line_margin)', 'sum(line_revenue)') }} as margin_pct
from items
-- Only report from the start date set in dbt_project.yml
where order_date >= '{{ var("reporting_start_date") }}'
group by order_date, category

with products as (
select generate_series('{{ var("reporting_start_date") }}', CURRENT_DATE, '1 Day'::interval)::date as date_day
)

select
p.date_day,
date_part('year',p.date_day) as date_year,
date_part('quarter',p.date_day) as date_quarter,
date_part('month',p.date_day) as date_month
from
products as p
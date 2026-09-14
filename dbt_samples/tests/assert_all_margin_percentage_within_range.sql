
select
*
from 
--analytics.mart_monthly_category_sales
{{ ref('mart_monthly_category_sales')}}
where
margin_pct < 0
or margin_pct > 100
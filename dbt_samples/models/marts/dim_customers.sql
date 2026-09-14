select
    customer_id,
    customer_name,
    segment,
    city,
    state,
    signup_date
from 
--analytics.stg_customers 
{{ ref('stg_customers') }}

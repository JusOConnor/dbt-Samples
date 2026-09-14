with source as (
    select
    *
    from
    --analytics.raw_products
    {{ source('foodservice', 'raw_products') }}
)

select
    product_id,
    product_name,
    initcap(category) as category,
    subcategory,
    brand,
    unit_of_measure,
    list_price,
    -- unit_cost is occasionally missing. We leave it as null here and decide how
    -- to handle it in the intermediate layer, closer to where margin is figured.
    unit_cost
from source

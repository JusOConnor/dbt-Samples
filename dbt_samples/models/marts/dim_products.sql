with products as (
    select
    * 
    from 
    --analytics.stg_products 
    {{ ref('stg_products') }}
),

departments as (
    select
    * 
    from
    --analytics.category_department_map 
    {{ ref('category_department_map') }}
)

select
    products.product_id,
    products.product_name,
    products.category,
    departments.department,
    products.subcategory,
    products.brand,
    products.unit_of_measure,
    products.list_price,
    products.unit_cost
from products
left join departments on products.category = departments.category

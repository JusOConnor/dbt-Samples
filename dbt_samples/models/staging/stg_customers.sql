with source as (
    select
    *
    from
    --analytics.raw_customers
    {{ source('foodservice', 'raw_customers') }}
),

cleaned as (
    select distinct
        customer_id,
        -- Names arrive in mixed case with stray spaces. Trim then title case
        -- turns 'CEDAR CATERING' and '  harvest grill  ' into one clean form.
        initcap(trim(customer_name)) as customer_name,
        segment,
        city,
        state,
        -- signup_date is text in two formats and is sometimes blank. We pick the
        -- parser based on whether the value contains a slash.
        case
            when signup_date is null or signup_date = '' then null
            when signup_date like '%/%' then to_date(signup_date, 'MM/DD/YYYY')
            else to_date(signup_date, 'YYYY-MM-DD')
        end as signup_date
    from source
)

select * from cleaned

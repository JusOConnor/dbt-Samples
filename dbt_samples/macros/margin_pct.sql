{% macro margin_pct(margin_expression, revenue_expression) %}

    case
        when {{ revenue_expression }} = 0 then 0
        else round(({{ margin_expression }} / {{ revenue_expression }} * 100)::numeric, 2)
    end
{% endmacro %}

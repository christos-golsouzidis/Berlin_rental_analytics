{% macro median(column) %}
    MEDIAN({{ column }})
{% endmacro %}
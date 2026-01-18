{{ config(materialized='table') }}

{% set start_date = '2020-01-01' %}
{% set end_date = '2026-12-31' %}

WITH dates AS (
    SELECT
        DATE '{{ start_date }}' + INTERVAL '1 day' * generate_series(0, DATE '{{ end_date }}' - DATE '{{ start_date }}') AS full_date
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INT AS date_key,
    full_date,
    EXTRACT(DOW FROM full_date) AS day_of_week,
    TO_CHAR(full_date, 'Day') AS day_name,
    EXTRACT(WEEK FROM full_date) AS week_of_year,
    EXTRACT(MONTH FROM full_date) AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(YEAR FROM full_date) AS year,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
FROM dates
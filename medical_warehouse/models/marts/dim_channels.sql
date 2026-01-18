{{ config(materialized='table') }}

WITH channel_stats AS (
    SELECT
        channel_name,
        'Pharmaceutical' AS channel_type,  -- Manually classify or derive
        MIN(message_date) AS first_post_date,
        MAX(message_date) AS last_post_date,
        COUNT(*) AS total_posts,
        AVG(views) AS avg_views
    FROM {{ ref('stg_telegram_messages') }}
    GROUP BY channel_name
)

SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,
    channel_name,
    channel_type,
    first_post_date,
    last_post_date,
    total_posts,
    avg_views
FROM channel_stats
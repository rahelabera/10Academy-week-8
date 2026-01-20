{{ config(materialized='table') }}

SELECT
    id.message_id,
    m.channel_key,
    m.date_key,
    id.detected_objects AS detected_class,
    id.confidence_scores AS confidence_score,
    id.image_category
FROM raw.image_detections id
JOIN {{ ref('fct_messages') }} m ON id.message_id = m.message_id AND id.channel_name = m.channel_name  -- Assuming channel_name in fct_messages or derive
SELECT *
FROM {{ ref('fct_messages') }}
WHERE message_date > CURRENT_DATE
SELECT *
FROM {{ ref('all_data_ready') }}
WHERE EXTRACT(YEAR FROM date) = 2023
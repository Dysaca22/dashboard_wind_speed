SELECT DISTINCT AVG(speed) OVER (PARTITION BY date) AS speed, date
FROM {{ ref('all_data_ready') }}
ORDER BY date
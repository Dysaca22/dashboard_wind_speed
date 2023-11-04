WITH regional_data AS (
  SELECT 
    date, 
    region,
    AVG(speed) OVER (PARTITION BY date, region) AS avg_speed
  FROM {{ ref('all_data_ready') }}
)

SELECT 
  date,
  MAX(IF(region = 'Amazonica', avg_speed, NULL)) AS Amazonica,
  MAX(IF(region = 'Andina', avg_speed, NULL)) AS Andina,
  MAX(IF(region = 'Caribe', avg_speed, NULL)) AS Caribe,
  MAX(IF(region = 'Orinoquia', avg_speed, NULL)) AS Orinoquia,
  MAX(IF(region = 'Pacifico', avg_speed, NULL)) AS Pacifico
FROM regional_data
GROUP BY date
ORDER BY date
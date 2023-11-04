WITH regional_data AS (
  SELECT 
    DATETIME(date, TIME(hour, 0, 0)) AS date, 
    region,
    AVG(direction) OVER (PARTITION BY date, hour, region) AS avg_direction
  FROM {{ ref('all_data_ready') }}
)

SELECT 
  date,
  MAX(IF(region = 'Amazonica', avg_direction, NULL)) AS Amazonica,
  MAX(IF(region = 'Andina', avg_direction, NULL)) AS Andina,
  MAX(IF(region = 'Caribe', avg_direction, NULL)) AS Caribe,
  MAX(IF(region = 'Orinoquia', avg_direction, NULL)) AS Orinoquia,
  MAX(IF(region = 'Pacifico', avg_direction, NULL)) AS Pacifico
FROM regional_data
GROUP BY date
ORDER BY date
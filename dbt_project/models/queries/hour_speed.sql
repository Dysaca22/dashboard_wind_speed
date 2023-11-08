WITH hour_speed AS (
  SELECT speed, EXTRACT(HOUR FROM date) AS hour
  FROM {{ ref('all_data_ready') }}
)

SELECT DISTINCT
  AVG(speed) OVER(PARTITION BY hour) AS avgSpeed, 
  PERCENTILE_CONT(speed, 0.5) OVER(PARTITION BY hour) AS medSpeed,
  hour
FROM hour_speed
ORDER BY hour
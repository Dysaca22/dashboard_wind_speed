WITH month_speed AS (
  SELECT speed, EXTRACT(MONTH FROM date) AS month
  FROM {{ ref('all_data_ready') }}
)

SELECT DISTINCT
  AVG(speed) OVER(PARTITION BY month) AS avgSpeed, 
  PERCENTILE_CONT(speed, 0.5) OVER(PARTITION BY month) AS medSpeed,
  month
FROM month_speed
ORDER BY month
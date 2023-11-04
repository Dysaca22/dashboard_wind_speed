SELECT 
  region, 
  EXTRACT(MONTH FROM date) AS month,
  AVG(speed) AS avg_speed, 
  MIN(speed) AS min_speed,
  MAX(speed) AS max_speed,
  APPROX_QUANTILES(speed, 100)[OFFSET(50)] AS median_speed,
  STDDEV(speed) AS dev_speed,
  AVG(direction) AS avg_direction,
  APPROX_QUANTILES(direction, 100)[OFFSET(50)] AS median_direction,
  STDDEV(direction) AS dev_direction
FROM {{ ref('all_data_ready') }}
GROUP BY region, EXTRACT(MONTH FROM date)
SELECT 
  COUNT(DISTINCT state) OVER () AS no_states,
  COUNT(DISTINCT department) OVER () AS no_departments,
  COUNT(DISTINCT region) OVER () AS no_regions,
  COUNT(DISTINCT code) OVER () AS no_stations,
  COUNT(*) OVER () AS no_records,
FROM {{ ref('all_data_ready') }}
LIMIT 1
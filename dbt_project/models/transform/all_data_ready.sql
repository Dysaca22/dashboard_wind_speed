SELECT speed_clean.* EXCEPT(speed), speed, direction 
FROM {{ ref('wind_speed_clean') }} speed_clean
INNER JOIN {{ ref('wind_direction_clean') }} direction_clean
USING(date, code)
ORDER BY date, code
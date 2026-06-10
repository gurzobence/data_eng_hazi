SELECT 
    actual_date, 
    max_temp_celsius, 
    precipitation_mm, 
    total_rides, 
    ROUND(avg_duration_minutes, 2) AS avg_duration
FROM agg_daily_rides
ORDER BY max_temp_celsius DESC
LIMIT 10;
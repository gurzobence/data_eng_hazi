SELECT 
    s.station_name, 
    COUNT(f.ride_id) AS total_departures
FROM fact_rides f
JOIN dim_station s ON f.start_station_id = s.station_id
GROUP BY s.station_name
ORDER BY total_departures DESC
LIMIT 5;
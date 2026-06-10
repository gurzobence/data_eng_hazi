SELECT 
    rider_type, 
    COUNT(ride_id) AS total_rides, 
    ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes
FROM fact_rides
GROUP BY rider_type;
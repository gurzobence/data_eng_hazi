
  
  create view "warehouse"."main"."agg_daily_rides__dbt_tmp" as (
    select
    w.actual_date,
    w.max_temp_celsius,
    w.precipitation_mm,
    count(f.ride_id) as total_rides,
    avg(f.duration_minutes) as avg_duration_minutes
from "warehouse"."main"."fact_rides" f
join "warehouse"."main"."dim_weather" w 
  on f.date_id = w.date_id
group by 1, 2, 3
  );

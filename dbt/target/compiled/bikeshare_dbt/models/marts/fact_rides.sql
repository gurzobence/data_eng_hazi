

select
    ride_id,
    start_time,
    end_time,
    date_diff('minute', start_time, end_time) as duration_minutes,
    start_station_id,
    end_station_id,
    strftime(start_time, '%Y%m%d')::integer as date_id,
    rider_type
from "warehouse"."main"."stg_bikeshare"
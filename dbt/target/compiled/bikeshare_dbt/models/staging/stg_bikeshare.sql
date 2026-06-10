

with raw_rides as (
    -- A DuckDB automatikusan kiolvassa az összes CSV-t a bikeshare mappából
    select * from read_csv_auto('s3://bronze/bikeshare/*.csv')
)

select
    ride_id,
    rideable_type,
    -- Típuskonverziók
    started_at::timestamp as start_time,
    ended_at::timestamp as end_time,
    
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    
    start_lat::double as start_lat,
    start_lng::double as start_lng,
    end_lat::double as end_lat,
    end_lng::double as end_lng,
    
    member_casual as rider_type
from raw_rides
where ride_id is not null
  and start_station_id is not null 
  and end_station_id is not null
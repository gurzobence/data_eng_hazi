{{ config(materialized='table') }}

with start_stations as (
    select start_station_id as station_id, start_station_name as station_name, start_lat as lat, start_lng as lng 
    from {{ ref('stg_bikeshare') }}
),
end_stations as (
    select end_station_id as station_id, end_station_name as station_name, end_lat as lat, end_lng as lng 
    from {{ ref('stg_bikeshare') }}
),
all_stations as (
    select * from start_stations
    union
    select * from end_stations
)

select
    station_id,
    max(station_name) as station_name,
    max(lat) as latitude,
    max(lng) as longitude
from all_stations
where station_id is not null
group by station_id
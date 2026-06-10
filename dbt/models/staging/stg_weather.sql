{{ config(materialized='table') }}

with raw_weather as (
    -- A json fájlok beolvasása a weather mappából
    select * from read_json_auto('s3://bronze/weather/*.json')
),

flattened_weather as (
    -- Az API válaszában a 'daily' egy struktúra, ami tömböket tartalmaz.
    -- Ezeket a tömböket az unnest() függvénnyel "szétterítjük" sorokká.
    select
        unnest(daily.time)::date as weather_date,
        unnest(daily.temperature_2m_max)::double as max_temp_celsius,
        unnest(daily.temperature_2m_min)::double as min_temp_celsius,
        unnest(daily.precipitation_sum)::double as precipitation_mm
    from raw_weather
)

select *
from flattened_weather
where weather_date is not null
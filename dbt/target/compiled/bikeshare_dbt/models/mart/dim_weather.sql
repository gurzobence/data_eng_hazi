select
    strftime(weather_date, '%Y%m%d')::integer as date_id,
    weather_date as actual_date,
    max_temp_celsius,
    min_temp_celsius,
    precipitation_mm
from "warehouse"."main"."stg_weather"
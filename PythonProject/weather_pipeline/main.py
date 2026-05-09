from datetime import datetime
import json
import os

from src.pipeline.transform import transform_from_hourly_to_daily_data, transform_to_hourly_data
from src.pipeline.load import load_to_dim_location, load_to_fact_weather_hourly, load_to_fact_weather_daily
from src.pipeline.extract import fetch_weather

cities = [
    {"name": "Hanoi"},
    {"name": "Da Nang"},
    {"name": "Tay Ninh"}
]
for city in cities:
    data = fetch_weather(cityname=city["name"])
    today = datetime.now().date()
    os.makedirs(f"data/{today}/raw", exist_ok=True)
    filename = f"data/{today}/raw/weather_data_of_{city['name']}.JSON"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    processed_hourly = transform_to_hourly_data(filename)
    processed_daily = transform_from_hourly_to_daily_data(processed_hourly)
    load_to_dim_location(processed_hourly)
    load_to_fact_weather_hourly(processed_hourly)
    load_to_fact_weather_daily(processed_hourly, processed_daily)
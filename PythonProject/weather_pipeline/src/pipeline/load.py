import json
from psycopg2.extras import execute_values

from src.database.connection import get_connection

def load_to_dim_location(data):
    conn = get_connection()
    cur = conn.cursor()

    records_dim_location = []
    records_dim_location.append((
        data["latitude"],
        data["longitude"],
        data["cityname"]))
    query1 = """INSERT INTO dim_location (latitude,longitude,city_name)
                VALUES %s
                ON CONFLICT(latitude, longitude)
                DO NOTHING
             """
    execute_values(cur,query1,records_dim_location)
    conn.commit()
    conn.close()
    cur.close()


def load_to_fact_weather_hourly(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""SELECT id FROM dim_location
                        WHERE latitude = {data["latitude"]} AND longitude = {data["longitude"]}
                """)
    dim_location_id = cur.fetchone()[0]
    records_fact_weather_hourly = []
    for i in range(len(data["hourly"]["time"])):
        records_fact_weather_hourly.append((
            dim_location_id,
            data["hourly"]["time"][i],
            data["hourly"]["temperature_2m"][i],
            data["hourly"]["wind_speed_10m"][i],
            data["hourly"]["wind_direction_10m"][i],
            data["hourly"]["relative_humidity_2m"][i],
            data["hourly"]["visibility"][i],
            data["hourly"]["rain"][i],
            data["hourly"]["precipitation_probability"][i],
            data["hourly"]["cloud_cover"][i],
            data["hourly"]["surface_pressure"][i],
            data["hourly"]["pressure_msl"][i]
        ))
    query2 = """INSERT INTO fact_weather_hourly(dim_location_id,datetime, temperature_2m, wind_speed, wind_direction, humidity_2m,
                                                visibility, rain, precipitation_probability, cloud_cover,
                                                surface_pressure, sea_level_pressure)
                VALUES %s
                ON CONFLICT (dim_location_id, datetime) DO NOTHING
             """
    execute_values(cur, query2, records_fact_weather_hourly)
    conn.commit()
    conn.close()
    cur.close()

def load_to_fact_weather_daily(processed_hourly_data,processed_daily_data):
    conn = get_connection()
    cur = conn.cursor()


    cur.execute(f"""SELECT id FROM dim_location
                            WHERE latitude = {processed_hourly_data["latitude"]} AND longitude = {processed_hourly_data["longitude"]}
                    """)
    dim_location_id = cur.fetchone()[0]


    records_fact_weather_daily = []
    for i in range(len(processed_daily_data["date"])):
        records_fact_weather_daily.append(
            (
                dim_location_id,
                processed_daily_data["date"][i],
                processed_daily_data["temperature_2m_max"][i],
                processed_daily_data["temperature_2m_min"][i],
                processed_daily_data["temperature_2m_mean"][i],
                processed_daily_data["relative_humidity_2m_mean"][i],
                processed_daily_data["surface_pressure_mean"][i],
                processed_daily_data["sea_level_pressure_mean"][i]
            )
        )

    query3 = """INSERT INTO fact_weather_daily(dim_location_id,date,temperature_2m_max,temperature_2m_min,temperature_2m_mean,relative_humidity_2m_mean,surface_pressure_mean,sea_level_pressure_mean)
                 VALUES %s
                 ON CONFLICT (dim_location_id, date) DO NOTHING
                 """
    execute_values(cur,query3,records_fact_weather_daily)
    conn.commit()
    conn.close()
    cur.close()



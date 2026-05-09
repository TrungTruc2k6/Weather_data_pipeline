import json
import  pandas as pd

def standardlizeCityName(cityname):

    standardlized_cityname = {
        "Da Nang": "Đà Nẵng",
        "Hanoi": "Hà Nội",
        "Tay Ninh": "Tây Ninh"
    }
    for name in standardlized_cityname:
        if cityname == name: cityname = standardlized_cityname[name]
    return cityname

def changeFarToCel(temperature):
    for i in range(len(temperature)):
        temperature[i] = round((temperature[i] - 32 )/1.8, 4)
    return temperature

def transform_from_hourly_to_daily_data(hourly_data):
    df_hourly = pd.DataFrame(hourly_data["hourly"])
    df_hourly["time"] = pd.to_datetime(df_hourly["time"])
    df_hourly["date"] = df_hourly["time"].dt.date

    df_daily = df_hourly.groupby("date").agg(
        temperature_2m_max=("temperature_2m", "max"),
        temperature_2m_min=("temperature_2m","min"),
        temperature_2m_mean=("temperature_2m", "mean"),
        relative_humidity_2m_mean=("relative_humidity_2m","mean"),
        surface_pressure_mean=("surface_pressure","mean"),
        sea_level_pressure_mean=("pressure_msl","mean")
        ).reset_index()
    df_daily["date"] = pd.to_datetime(df_daily["date"]).dt.date
    return df_daily

def transform_to_hourly_data(fileJSON):
    with open(fileJSON,"r") as f:
        data = json.load(f)
        data["cityname"] = standardlizeCityName(data["cityname"])
        data["hourly"]["temperature_2m"] = changeFarToCel(data["hourly"]["temperature_2m"])
        return data




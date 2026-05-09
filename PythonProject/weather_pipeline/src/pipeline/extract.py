from http.client import responses

import requests

def get_lat_and_long(cityname):
    weather_data  = []
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name":cityname
    }
    response = requests.get(url,params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data.append({"lat":data["results"][0]["latitude"],
                            "lon":data["results"][0]["longitude"]})
    else:
        print(f"Error fetching data for {cityname}: {response.status_code}")
    return weather_data

def fetch_weather(cityname):
    coordCities = get_lat_and_long(cityname)
    lat = coordCities[0]["lat"]
    long = coordCities[0]["lon"]

    url = "https://api.open-meteo.com/v1/forecast"
    param = {
        "latitude": lat,
        "longitude": long,
        "hourly":  ["", "temperature_2m",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "relative_humidity_2m",
                    "visibility",
                    "rain",
                    "precipitation_probability",
                    "cloud_cover",
                    "surface_pressure",
                    "pressure_msl"],
        "temperature_unit": "fahrenheit"
    }
    response = requests.get(url,params=param)
    if response.status_code == 200:
        data = response.json()
        data["cityname"] = cityname
        return data
    else:
        print(f"Error fetching data for {cityname}: {response.status_code}")

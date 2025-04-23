# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import date, timedelta

cities = {
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Moscow": (55.7558, 37.6173)
}

start_date = (date.today() - timedelta(days=30)).isoformat()
end_date = date.today().isoformat()

all_data = []

for city, (lat, lon) in cities.items():
    url = f"https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "UTC"
    }
    r = requests.get(url, params=params)
    json_data = r.json()
    df = pd.DataFrame(json_data["daily"])
    df["city"] = city
    all_data.append(df)

df_all = pd.concat(all_data)
df_all.to_csv("weather_data.csv", index=False)
print("Данные сохранены в weather_data.csv")

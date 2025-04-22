# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime, timedelta

cities = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Moscow": (55.7558, 37.6173),
    "Baku": (40.4092, 49.8670)
}

end_date = datetime.today()
start_date = end_date - timedelta(days=30)

df_list = []
for city, (lat, lon) in cities.items():
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date:%Y-%m-%d}&end_date={end_date:%Y-%m-%d}&daily=temperature_2m_max&timezone=auto"
    res = requests.get(url).json()
    for date, temp in zip(res["daily"]["time"], res["daily"]["temperature_2m_max"]):
        df_list.append({
            "city": city,
            "date": date,
            "temperature": temp
        })

df = pd.DataFrame(df_list)
df.to_csv("weather_data.csv", index=False)
print("Weather data saved to weather_data.csv")

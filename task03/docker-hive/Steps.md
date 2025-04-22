1. git clone <https://github.com/big-data-europe/docker-hive>
2. S:\BiG_DATA\Big_Data\Big_Data_DZ\task03> mkdir scripts
3. S:\BiG_DATA\Big_Data\Big_Data_DZ\task03> mv scripts docker-hive
4. S:\BiG_DATA\Big_Data\Big_Data_DZ\task03> cd .\docker-hive\
5. S:\BiG_DATA\Big_Data\Big_Data_DZ\task03\docker-hive> cd .\scripts\
6. echo > fetch_weather.py

    ```python

    # scripts/fetch_weather.py

    import requests
    import pandas as pd
    from datetime import datetime, timedelta

    cities = {
        "New York": (40.7128, -74.0060),
        "London": (51.5074, -0.1278),
        "Tokyo": (35.6895, 139.6917),
        "Sydney": (-33.8688, 151.2093),
        "Moscow": (55.7558, 37.6173),
        "Baku": (40.409264, 49.867092)
    }

    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    df_list = []
    for city, (lat, lon) in cities.items():
        url = f"<https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date:%Y-%m-%d}&end_date={end_date:%Y-%m-%d}&daily=temperature_2m_max&timezone=auto>"
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
    ```

7. echo > plot_weather.py

```python
    # scripts/plot_weather.py
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv("weather_data.csv")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="date", y="temperature", hue="city")
    plt.title("Температура по городам за последний месяц")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("weather_by_city.png")
    plt.clf()

    sns.histplot(df["temperature"], bins=30, kde=True)
    plt.title("Распределение температур")
    plt.savefig("temperature_distribution.png")
    print("Графики сохранены")

```

8. docker-compose up -d
9. docker exec -it python bash
10. pip install pandas matplotlib seaborn requests
11. python fetch_weather.py
12. python plot_weather.py
13. exit

* Сохранить результаты в HDFS

14. docker cp scripts/weather_data.csv namenode:/tmp/
15. docker exec -it namenode bash
16. hdfs dfs -ls /
17. hdfs dfs -mkdir -p /data/weather
18. hdfs dfs -put /tmp/weather_data.csv /data/weather/

* Проверка, что файл в HDFS

19. hdfs dfs -ls /data/weather

* Выгружаем из HDFS обратно на локальную машину

20. docker exec -it namenode bash
21. mkdir -p /scripts
22. hdfs dfs -get /data/weather/weather_data.csv /scripts/weather_data_from_hdfs.csv
23. exit
24. docker cp namenode:/scripts/weather_data_from_hdfs.csv ./scripts/weather_data_from_hdfs.csv

1. git clone <https://github.com/big-data-europe/docker-hive>
2. cd task03.2
3. cd .\docker-hive\
4. docker-compose up -d

5. docker exec -it superset bash
6. pip install psycopg2-binary
7. exit
8. docker restart superset

9. Cоздаем : superset.Dockerfile для подключения Hive/Presto

```text
FROM apache/superset:latest

USER root
RUN pip install --no-cache-dir psycopg2-binary
# Установим Hive и Presto драйверы
RUN pip install "apache-superset[apache-hive]" "apache-superset[presto]"

USER superset
```

10. docker-compose up --build -d
11. <http://localhost:8088>
12. <http://localhost:8088/login/>
13. admin admin
14. Display Name: Aurora PostgreSQL (Data API)
15. SQLAlchemy URI: postgresql+psycopg2://hive:hive@host.docker.internal:5432/metastore
16. SQLAlchemy URI: presto://presto:8080/hive/default
17. SQLAlchemy URI: hive://hive-server:10000/default
18. /scripts/weather_fetcher.py
19. docker exec -it python python weather_fetcher.py
20. docker exec -it python bash
19. apt update && apt install -y python3-pip
20. pip install requests pandas
21. python /scripts/weather_fetcher.py
22. cd ..
23. ls    bin   dev  home  lib64  mnt  proc  run   scripts  sys  usr  weather_data.csv
24. mv weather_data.csv /scripts/

####

25. docker cp scripts/weather_data.csv namenode:/tmp/
26. docker exec -it namenode bash
27. hdfs dfs -ls /
28. hdfs dfs -mkdir -p /data/weather
29. hdfs dfs -put /tmp/weather_data.csv /data/weather/
30. exit

#####

31. docker exec -it hive-server bash
32. hive

33. ```sql

    CREATE EXTERNAL TABLE IF NOT EXISTS weather_data (
        `date` STRING,
        temperature_2m_max DOUBLE,
        temperature_2m_min DOUBLE,
        city STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '/data/weather';


        -- Проверка
        SELECT * FROM weather_data LIMIT 10;
    ```

    exit;
    exit

####

34. Database: Presto
    Schema: default
    Table: weather_data

35. Line Chart по date, цвет по city, метрика AVG(temperature_2m_max)
36. Histogram по temperature_2m_max

37. docker exec -it namenode bash
38. ls /tmp
39. exit
40. docker cp namenode:/tmp/weather_data.csv ./scripts/weather_data_from_hdfs.csv

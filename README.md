## 1. DZ_1

```text
Сделайте mapper и reducer, чтобы посчитать среднее и дисперсию оценок за фильм.
```

## 2. DZ_2

```text
Урок 2. SQL & Big Data
Условие:
Загрузите датасет по ценам на жилье Airbnb, доступный на kaggle.com: https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data
Подсчитайте среднее значение и дисперсию по признаку ”price” в hive
Используя Python, реализуйте скрипт mapper.py и reducer.py для расчета
Проверьте правильность подсчета статистики методом mapreduce в сравнении со hive.

```

### Последовательность действий: task02\docker-hive\Steps.md

1. Удали все текущие контейнеры и образы, если они уже созданы:

* docker-compose down -v
* docker system prune -af

2. git clone <https://github.com/big-data-europe/docker-hive>

3. docker-compose up -d

4. Предположим, скачал файл как AB_NYC_2019.csv

* docker cp scripts/AB_NYC_2019.csv namenode:/tmp/

5. Теперь загрузим его в HDFS внутри контейнера:

* docker exec -it namenode bash
* hdfs dfs -mkdir -p /user/hive/warehouse/airbnb
* hdfs dfs -put /tmp/AB_NYC_2019.csv /user/hive/warehouse/airbnb/
* exit

6. Hive: рассчитать среднее и дисперсию:

* 1. docker exec -it hive-server bash
* 2. hive

* ```sql
    CREATE EXTERNAL TABLE airbnb (
    id INT,
    name STRING,
    host_id INT,
    host_name STRING,
    neighbourhood_group STRING,
    neighbourhood STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    room_type STRING,
    price INT,
    minimum_nights INT,
    number_of_reviews INT,
    last_review STRING,
    reviews_per_month DOUBLE,
    calculated_host_listings_count INT,
    availability_365 INT

    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    TBLPROPERTIES ("skip.header.line.count"="1");

    LOAD DATA INPATH '/user/hive/warehouse/airbnb/AB_NYC_2019.csv' INTO TABLE airbnb;

    ```

* Теперь расчёт:

```sql
    SELECT AVG(price), VARIANCE(price) FROM airbnb;
```

```sql
    SELECT
        ROUND(AVG(price), 2) AS mean_price,
        ROUND(VARIANCE(price), 2) AS variance_price
    FROM airbnb;
```

```text
    Mean:     145.12  
    Variance: 58528.67

    mean_price | variance_price
    -----------|----------------
       142.12  |   58528.67
```

7. Запуск MapReduce(вариант 2):

* docker exec -it python bash
* cat AB_NYC_2019.csv | python mapper.py | sort | python reducer.py
* python mapper.py < AB_NYC_2019.csv | sort | python reducer.py

```text
Mean:     152.72  
Variance: 57672.85
```

``` docker-compose.yaml

version: "5"

services:
namenode:
image: bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8
volumes:
    - namenode:/hadoop/dfs/name
environment:
    - CLUSTER_NAME=test
env_file:
    - ./hadoop-hive.env
ports:
    - "50070:50070"

datanode:
image: bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
volumes:
    - datanode:/hadoop/dfs/data
env_file:
    - ./hadoop-hive.env
environment:
    SERVICE_PRECONDITION: "namenode:50070"
ports:
    - "50075:50075"

hive-server:
image: bde2020/hive:2.3.2-postgresql-metastore
env_file:
    - ./hadoop-hive.env
environment:
    HIVE_CORE_CONF_javax_jdo_option_ConnectionURL: "jdbc:postgresql://hive-metastore/metastore"
    SERVICE_PRECONDITION: "hive-metastore:9083"
ports:
    - "10000:10000"

hive-metastore:
image: bde2020/hive:2.3.2-postgresql-metastore
env_file:
    - ./hadoop-hive.env
command: /opt/hive/bin/hive --service metastore
environment:
    SERVICE_PRECONDITION: "namenode:50070 datanode:50075 hive-metastore-postgresql:5432"
ports:
    - "9083:9083"

hive-metastore-postgresql:
image: bde2020/hive-metastore-postgresql:2.3.0

presto-coordinator:
image: shawnzhu/prestodb:0.181
ports:
    - "8080:8080"

python:
image: python:3.11-slim
container_name: python
command: tail -f /dev/null
volumes:
    - ./scripts:/scripts
working_dir: /scripts
tty: true
stdin_open: true

volumes:
namenode:
datanode:


 ```

## 3. DZ_3

```text
Домашнее задание

1. Соберите данные о погоде в разных городах мира за последний месяц.
Используйте открытые источники данных, такие как API погодных
сервисов или веб-скрейпинг.

2. Выведете график изменения температуры в разных городах, график
распределения температуры.
3. Сохранить результаты в HDFS
4. Выгрузить результаты из HDFS на локальный компьютер
```

Решение с помошью Pandas, без Superset.
Использую контейнер из прошлой домашки DZ2

1. git clone <https://github.com/big-data-europe/docker-hive>
2. mkdir scripts
3. mv scripts docker-hive
4. cd .\docker-hive\
5. cd .\scripts\
6. echo > fetch_weather.py
7. echo > plot_weather.py
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

* Проверка , что файл в HDFS

19. hdfs dfs -ls /data/weather

* Выгружаем из HDFS обратно на локальную машину

20. docker exec -it namenode bash
21. mkdir -p /scripts
22. hdfs dfs -get /data/weather/weather_data.csv /scripts/weather_data_from_hdfs.csv
23. exit
24. docker cp namenode:/scripts/weather_data_from_hdfs.csv ./scripts/weather_data_from_hdfs.csv

## 3. DZ_3.2

#### Визуализация погодных данных с помощью Superset, Hive и Presto

```test
В этом проекте собираются погодные данные из открытого API, сохраняются в CSV, загружаются в HDFS и визуализируются с помощью Superset. Hive и Presto используются для обработки данных.
```

#### Steps

    Подготовка среды:
    Если вы запускаете проект не в первый раз — очистите старые контейнеры и образы (новичкам этот шаг можно пропустить):

1. docker-compose down -v
2. docker system prune -af

3. Клонирование репозитория:

* git clone <https://github.com/big-data-europe/docker-hive>

        Немного изменил docker-compose.yml
        добавил superset и рядом с docker-compose.yml создал superset.Dockerfile для установки драйвнров, чтобы superset подключить к Hive и Presto, а таккже к postgresql(hive-metastore-postgresql-в моем случаи)

4. Обновлённый docker-compose.yml и superset.Dockerfile
Добавлены:

* Superset

* Поддержка Presto, Hive и PostgreSQL для Superset

* Python-контейнер для запуска скриптов

<details> <summary>Показать docker-compose.yml и Dockerfile(Нажми, чтобы раскрыть)</summary>

``` docker

version: "5"

services:
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8
    container_name: namenode
    volumes:
      - namenode:/hadoop/dfs/name
    environment:
      - CLUSTER_NAME=test
    env_file:
      - ./hadoop-hive.env
    ports:
      - "50070:50070"

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
    container_name: datanode
    volumes:
      - datanode:/hadoop/dfs/data
    env_file:
      - ./hadoop-hive.env
    environment:
      SERVICE_PRECONDITION: "namenode:50070"
    ports:
      - "50075:50075"

  hive-metastore-postgresql:
    image: bde2020/hive-metastore-postgresql:2.3.0
    container_name: hive-metastore-postgresql
    ports:
      - "5432:5432"

  hive-metastore:
    image: bde2020/hive:2.3.2-postgresql-metastore
    container_name: hive-metastore
    command: /opt/hive/bin/hive --service metastore
    env_file:
      - ./hadoop-hive.env
    environment:
      SERVICE_PRECONDITION: "namenode:50070 datanode:50075 hive-metastore-postgresql:5432"
    ports:
      - "9083:9083"

  hive-server:
    image: bde2020/hive:2.3.2-postgresql-metastore
    container_name: hive-server
    env_file:
      - ./hadoop-hive.env
    environment:
      HIVE_CORE_CONF_javax_jdo_option_ConnectionURL: "jdbc:postgresql://hive-metastore/metastore"
      SERVICE_PRECONDITION: "hive-metastore:9083"
    ports:
      - "10000:10000"

  presto-coordinator:
    image: shawnzhu/prestodb:0.181
    container_name: presto
    ports:
      - "8080:8080"

  python:
    image: python:3.11-slim
    container_name: python
    command: tail -f /dev/null
    volumes:
      - ./scripts:/scripts
    working_dir: /scripts
    tty: true
    stdin_open: true

  superset:
    build:
      context: .
      dockerfile: superset.Dockerfile
    container_name: superset
    environment:
      - SUPERSET_SECRET_KEY=mysecretkey
      - DATABASE_URL=sqlite:////app/superset_home/superset.db
    ports:
      - "8088:8088"
    volumes:
      - superset_home:/app/superset_home
    depends_on:
      - presto-coordinator
    command: >
      /bin/bash -c "
      superset db upgrade &&
      superset fab create-admin --username admin --firstname Superset --lastname Admin --email <admin@superset.com> --password admin &&
      superset init &&
      superset run -h 0.0.0.0 -p 8088"

volumes:
  namenode:
  datanode:
  superset_home:

```

superset.Dockerfile:

```Dockerfile

    FROM apache/superset:latest

    USER root
    RUN pip install --no-cache-dir psycopg2-binary
    # Установим Hive и Presto драйверы
    RUN pip install "apache-superset[apache-hive]" "apache-superset[presto]"

    USER superset

```

5. Заходим в папку на локальном PC:

* cd task03.2
* cd .\docker-hive\
* mkdir /scripts - будет создана автоматически после запуска
* echo > weather_fetcher.py

6. Запускаем: docker-compose up -d
7. Нужно создать weather_data.csv, в этом файле будут соханины данные о погоде, котрые понадобятся для создания таблицы.
Для этого нужно запустить скрипт на Python: weather_fetcher.py
Этот кркипт был создан локально и находится в папе: /scripts/weather_fetcher.py. При этом, так как мы соединилди папку локальной машине и контейнера python, в контейнер также будет добавлен этот скрипт:
    * volumes:
      * ./scripts:/scripts
      * working_dir: /scripts

* docker exec -it python bash
* apt update && apt install -y python3-pip
* pip install requests pandas - забыл добавить pandas
* python /scripts/weather_fetcher.py
* cd ..
* ls - немного промохнулся с папкой и файл нужно переместить
* Результат вывода ls: bin   dev  home  lib64  mnt  proc  run   scripts  sys  usr  weather_data.csv
* mv weather_data.csv /scripts/
* теперь все на месте и в папке  /scripts/ в контейнере и PC появится weather_data.csv

8. Можно переходить к создание таблицы, но для начала нужно разместить файл в ноде:

* В ноду, копируем созданный скриптом файл - weather_data.csv.(Немного неуклюжо получилось)
* docker cp scripts/weather_data.csv namenode:/tmp/
* Заходим в ноду, точнее в контейнер с нодой.
* docker exec -it namenode bash
* Глянем содержимое.
* hdfs dfs -ls /
* Создаем папку и кладем туда наш weather_data.csv файл.
* hdfs dfs -mkdir -p /data/weather
* hdfs dfs -put /tmp/weather_data.csv /data/weather/
* exit

9. Создание таблицы в Hive:

* Заходим в hive-server:
* docker exec -it hive-server bash
* hive
* Создаем таблицу:

```sql

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

* exit; - выходим из sql
* exit  - выходим из hive-server

10. Основна работа сделана, нужно зайти в Superset и создать наши графики:

* Проходим по этому адресу в браузере:
* <http://localhost:8088>
* <http://localhost:8088/login/>
* login: admin password: admin
* Зашли, теперь нужно подключиться к базам данных, для этого найдите справа  Data → Databases → + Database (приложил картинки в Images c поэтапным подключением)
* У меня сразу отобразились 3 БД:
* Connect a database:
* PostgeSQL + рабочая
* Presto +  рабочая - дальше я буду использовать Presto
* SQLite - не рабочая
* Для PostgeSQL:
* Display Name: Aurora PostgreSQL (Data API)
* SQLAlchemy URI: postgresql+psycopg2://hive:hive@host.docker.internal:5432/metastore
* Проверяем TEST CONNECTION - жмем кнопку
* Дожно показать: Connection looks good!
* Аналогично для Presto:
* SQLAlchemy URI: presto://presto:8080/hive/default
* SQLAlchemy URI: hive://hive-server:10000/default -  с hive, на данном этапе, у меня не получилось

11. Нужно создать датасет и диаграммы:

* Для этого выбераем:
* DATABASE: Presto
* SCHEMA: default
* TABLE: weather_data:
  * Table columns:
    * Column name:
      * date
      * temperature_2m_max
      * temperature_2m_min
      * city
* Charts->Create a new chart->Choose a dataset(weather_data)->Choose charts type
* Для начала создадим: Line chart:
  * X-AXIS: data
  * METRICS: AVG(temperature_2m_max)
  * DIMENSIONS: city
* Save as->Chart Name->weather_data_line_chart
* Далее создадим Bar chart и histogram(подробно описывать не буду, создается аналогичным способом, толко привиду картинки в Images и weather-data-2025-04-23T01-37-59.161Z.pdf - результат того, что получилось)

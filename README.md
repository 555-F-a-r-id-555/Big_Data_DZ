## 1. DZ_1

```text
Сделайте mapper и reducer, чтобы посчитать среднее и дисперсию оценок за фильм.
```

## 1. DZ_2

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

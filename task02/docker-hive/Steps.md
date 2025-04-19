1. Удали все текущие контейнеры и образы:

* docker-compose down -v
* docker system prune -af

2. git clone <https://github.com/big-data-europe/docker-hive>

3. docker-compose up -d

4. Предположим, скачал файл как AB_NYC_2019.csv

* docker cp AB_NYC_2019.csv namenode:/tmp/
* docker cp AB_NYC_2019.csv docker-hive-namenode-1:/tmp/

5. Теперь загрузим его в HDFS внутри контейнера:

* 1. docker exec -it namenode bash
* 2. docker exec -it docker-hive-namenode-1 bash
* 1. hdfs dfs -mkdir -p /user/hive/warehouse/airbnb
* 2. docker exec -it docker-hive-namenode-1 hdfs dfs -mkdir -p /data/airbnb
* 1. hdfs dfs -put /tmp/AB_NYC_2019.csv /user/hive/warehouse/airbnb/
* 2. docker exec -it docker-hive-namenode-1 hdfs dfs -put /tmp/AB_NYC_2019.csv /data/airbnb/
* exit

6. Hive: рассчитать среднее и дисперсию:

* 1. docker exec -it hive bash
* 2. docker exec -it docker-hive-hive-server-1 bash
* 1. beeline -u jdbc:hive2://localhost:10000
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

* ```sql
    SHOW TABLES;
    SELECT COUNT(*) FROM airbnb;
    SELECT AVG(price), VARIANCE(price) FROM airbnb;
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

7. Запуск MapReduce:

* docker cp mapper.py docker-hive-namenode-1:/tmp/
* docker cp mapper.py docker-hive-namenode-1:/tmp/mapper.py
* docker cp reducer.py docker-hive-namenode-1:/tmp/
* docker cp reducer.py docker-hive-namenode-1:/tmp/reducer.py

* docker exec -it docker-hive-namenode-1 bash
  * hadoop version
  * which hadoop
  * root@2944980061eb:/# which hadoop
    /opt/hadoop-2.7.4/bin//hadoop

  * hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input /data/airbnb/AB_NYC_2019.csv \
        -output /output/airbnb_stats \
        -mapper "python3 /tmp/mapper.py" \
        -reducer "python3 /tmp/reducer.py" \
        -file /tmp/mapper.py \
        -file /tmp/reducer.py

  * hadoop jar /opt/hadoop-2.7.4/share/hadoop/tools/lib/hadoop-streaming-2.7.4.jar \
        -input /data/airbnb/AB_NYC_2019.csv \
        -output /output/airbnb_stats \
        -mapper "python3 /tmp/mapper.py" \
        -reducer "python3 /tmp/reducer.py" \
        -file /tmp/mapper.py \
        -file /tmp/reducer.py

* which python3
* apt update
* apt install -y python3

* результат:
* hdfs dfs -cat /output/airbnb_stats/part-00000

7. 2  Запуск MapReduce(вариант 2):

* docker exec -it python bash
* python script.py
* cat AB_NYC_2019.csv | python mapper.py | sort | python reducer.py
* python mapper.py < AB_NYC_2019.csv | sort | python reducer.py

``` docker-compose.yaml

version: "3"

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

```docker-compose.yaml

version: "3"

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

volumes:
  namenode:
  datanode:

```

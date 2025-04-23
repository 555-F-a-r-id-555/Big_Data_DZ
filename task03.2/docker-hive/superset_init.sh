#!/bin/bash

# Инициализация Superset
superset db upgrade
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin || true
superset init

# Добавление источника данных Hive
superset datasource add --database-name hive \
    --sqlalchemy-uri "hive://hive-server:10000/default" || true

# Добавление источника данных Presto
superset datasource add --database-name presto \
    --sqlalchemy-uri "presto://presto:8080/hive/default" || true

# Запуск Superset
superset run -h 0.0.0.0 -p 8088

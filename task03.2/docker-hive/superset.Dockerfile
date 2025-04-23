FROM apache/superset:latest

USER root
RUN pip install --no-cache-dir psycopg2-binary
# Установим Hive и Presto драйверы
RUN pip install "apache-superset[apache-hive]" "apache-superset[presto]"

USER superset

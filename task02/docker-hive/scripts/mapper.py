#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
next(reader)  # Пропустить заголовок
for row in reader:
    try:
        price = float(row[9])  # поле 'price'
        print(f"1\t{price}\t{price ** 2}")
    except:
        continue

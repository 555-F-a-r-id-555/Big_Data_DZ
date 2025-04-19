#!/usr/bin/env python3
import sys

n = 0
sum_price = 0.0
sum_sq_price = 0.0

for line in sys.stdin:
    count, price, sq_price = map(float, line.strip().split("\t"))
    n += int(count)
    sum_price += price
    sum_sq_price += sq_price

mean = sum_price / n
variance = (sum_sq_price / n) - (mean ** 2)
print(f"Mean: {mean:.2f}")
print(f"Variance: {variance:.2f}")

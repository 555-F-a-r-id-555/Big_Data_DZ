# -*- coding: utf-8 -*-
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

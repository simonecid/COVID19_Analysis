import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np
import os
import matplotlib.dates as mdates

if not os.path.isdir("plots"):
  os.mkdir("plots")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

province = ["MI", "CO", "VA", "LC", "BG"]

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
df["data"] = pd.to_datetime(df["data"])

df_filtered = df[["data", "sigla_provincia","totale_casi"]]

df_provinces = [df_filtered[df_filtered["sigla_provincia"] == pv] for pv in province]

for df_province in df_provinces:
  ax.plot(df_province.data, df_province.totale_casi)

ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

ax.legend(province)
ax.set_ylabel("# tamponi positivi")
ax.set_title("Numero di casi positivi totale in alcune province")
ax.grid()
plt.xticks(rotation=90)
fig.savefig("plots/Italy_ProvinceComparison_IT.png")

ax.set_title("Total number of positives in some provinces")
ax.set_ylabel("# positives")
fig.savefig("plots/Italy_ProvinceComparison_EN.png")
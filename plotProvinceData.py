import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

province = ["MI", "CO", "VA", "LC"]

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
df["data"] = pd.to_datetime(df["data"]).dt.date

df_filtered = df[["data", "sigla_provincia","totale_casi"]]

df_provinces = [df_filtered[df_filtered["sigla_provincia"] == pv] for pv in province]

for df_province in df_provinces:
  df_province.plot(x="data", y="totale_casi", ax=ax)

ax.legend(province)
ax.set_ylabel("# tamponi")
ax.grid()
plt.xticks(rotation=90)
fig.savefig("plots/Italy_ProvinceComparison_IT.png")

ax.set_ylabel("# tests")
fig.savefig("plots/Italy_ProvinceComparison_EN.png")
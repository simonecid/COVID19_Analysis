import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np
import os
import matplotlib.dates as mdates

if not os.path.isdir("plots"):
  os.mkdir("plots")

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df["data"] = pd.to_datetime(df["data"])


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

df_fullbreakdown = df[["data", "tamponi","terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
df_fullbreakdown["negativi"] = df_fullbreakdown["tamponi"] - df_fullbreakdown["terapia_intensiva"] - df_fullbreakdown["ricoverati_con_sintomi"] - df_fullbreakdown["isolamento_domiciliare"] - df_fullbreakdown["dimessi_guariti"] - df_fullbreakdown["deceduti"]
df_fullbreakdown = df_fullbreakdown.drop("tamponi", 1)
# ax = df_fullbreakdown.plot.bar(x="data", stacked=True) borken

ax.bar(df_fullbreakdown.data, df_fullbreakdown.terapia_intensiva)
ax.bar(df_fullbreakdown.data, df_fullbreakdown.ricoverati_con_sintomi, bottom=df_fullbreakdown.terapia_intensiva)
ax.bar(df_fullbreakdown.data, df_fullbreakdown.isolamento_domiciliare, bottom=df_fullbreakdown.terapia_intensiva + df_fullbreakdown.ricoverati_con_sintomi)
ax.bar(df_fullbreakdown.data, df_fullbreakdown.dimessi_guariti, bottom=df_fullbreakdown.terapia_intensiva + df_fullbreakdown.ricoverati_con_sintomi + df_fullbreakdown.isolamento_domiciliare)
ax.bar(df_fullbreakdown.data, df_fullbreakdown.deceduti, bottom=df_fullbreakdown.terapia_intensiva + df_fullbreakdown.ricoverati_con_sintomi + df_fullbreakdown.isolamento_domiciliare + df_fullbreakdown.dimessi_guariti )
ax.bar(df_fullbreakdown.data, df_fullbreakdown.negativi, bottom=df_fullbreakdown.terapia_intensiva + df_fullbreakdown.ricoverati_con_sintomi + df_fullbreakdown.isolamento_domiciliare + df_fullbreakdown.dimessi_guariti + df_fullbreakdown.deceduti)
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

ax.set_title("Italian tests breakdown")
ax.set_ylabel("# tests")
ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths", "Negatives"])
ax.grid(axis="y")
fig.savefig("plots/Italy_FullBreakdown_EN.png")


ax.set_title("Casistica dei tamponi in Italia")
ax.set_ylabel("# tamponi")
ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti", "Negativi"])
ax.grid(axis="y")
fig.savefig("plots/Italy_FullBreakdown_IT.png")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

df_breakdown = df[["data", "terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
# ax = df_breakdown.plot.bar(x="data", stacked=True) borken
ax.bar(df_breakdown.data, df_breakdown.terapia_intensiva)
ax.bar(df_breakdown.data, df_breakdown.ricoverati_con_sintomi, bottom=df_breakdown.terapia_intensiva)
ax.bar(df_breakdown.data, df_breakdown.isolamento_domiciliare, bottom=df_breakdown.terapia_intensiva + df_breakdown.ricoverati_con_sintomi)
ax.bar(df_breakdown.data, df_breakdown.dimessi_guariti, bottom=df_breakdown.terapia_intensiva + df_breakdown.ricoverati_con_sintomi + df_breakdown.isolamento_domiciliare)
ax.bar(df_breakdown.data, df_breakdown.deceduti, bottom=df_breakdown.terapia_intensiva + df_breakdown.ricoverati_con_sintomi + df_breakdown.isolamento_domiciliare + df_breakdown.dimessi_guariti)
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

ax.set_title("Italian tests breakdown (excluding negatives)")
ax.set_ylabel("# tests")
ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths", "Negatives"])
ax.grid(axis="y")
fig.savefig("plots/Italy_Breakdown_EN.png")

ax.set_title("Casistica dei tamponi in Italia (eccetto negativi)")
ax.set_ylabel("# tamponi")
ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti", "Negativi"])
ax.grid(axis="y")
fig.savefig("plots/Italy_Breakdown_IT.png")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

df_relative = df[["data","tamponi", "terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
df_relative["terapia_intensiva"] = df_relative["terapia_intensiva"]/df_relative["tamponi"]
df_relative["ricoverati_con_sintomi"] = df_relative["ricoverati_con_sintomi"]/df_relative["tamponi"]
df_relative["isolamento_domiciliare"] = df_relative["isolamento_domiciliare"]/df_relative["tamponi"]
df_relative["dimessi_guariti"] = df_relative["dimessi_guariti"]/df_relative["tamponi"]
df_relative["deceduti"] = df_relative["deceduti"]/df_relative["tamponi"]
df_relative = df_relative.drop("tamponi", 1)
# ax = df_relative.plot.bar(x="data", stacked=True) borken
ax.bar(df_relative.data, df_relative.terapia_intensiva)
ax.bar(df_relative.data, df_relative.ricoverati_con_sintomi, bottom=df_relative.terapia_intensiva)
ax.bar(df_relative.data, df_relative.isolamento_domiciliare, bottom=df_relative.terapia_intensiva + df_relative.ricoverati_con_sintomi)
ax.bar(df_relative.data, df_relative.dimessi_guariti, bottom=df_relative.terapia_intensiva + df_relative.ricoverati_con_sintomi + df_relative.isolamento_domiciliare)
ax.bar(df_relative.data, df_relative.deceduti, bottom=df_relative.terapia_intensiva + df_relative.ricoverati_con_sintomi + df_relative.isolamento_domiciliare + df_relative.dimessi_guariti)
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

ax.set_title("Italian tests breakdown relative to total number of tests")
ax.set_ylabel("Fraction w.r.t. total tests")
ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths"])
ax.grid(axis="y")
fig.savefig("plots/Italy_Breakdown_Relative_EN.png")

ax.set_title("Casistica percentuale dei tamponi in Italia")
ax.set_ylabel("Frazione dei tamponi totali")
ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti"])
ax.grid(axis="y")
fig.savefig("plots/Italy_Breakdown_Relative_IT.png")
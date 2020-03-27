import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np

# regions = ["Lombardia", "Veneto"]
regions = ["Lombardia", "Veneto"]

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
df["data"] = pd.to_datetime(df["data"]).dt.date

df_regions = [ df[df["denominazione_regione"] == region] for region in regions]

for index, df_region in enumerate(df_regions):
  region = regions[index]

  df_fullbreakdown = df_region[["data", "tamponi","terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
  df_fullbreakdown["negativi"] = df_fullbreakdown["tamponi"] - df_fullbreakdown["terapia_intensiva"] - df_fullbreakdown["ricoverati_con_sintomi"] - df_fullbreakdown["isolamento_domiciliare"] - df_fullbreakdown["dimessi_guariti"] - df_fullbreakdown["deceduti"]
  df_fullbreakdown = df_fullbreakdown.drop("tamponi", 1)
  ax = df_fullbreakdown.set_index("data").plot.bar(stacked=True)
  ax.grid(axis="y")


  ax.set_title(region + " tests breakdown")
  ax.set_ylabel("# tests")
  ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths", "Negatives"])
  plt.savefig("plots/" + region + "_FullBreakdown_EN.png")

  ax.set_title("Casistica dei tamponi in " + region)
  ax.set_ylabel("# tamponi")
  ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti", "Negativi"])
  plt.savefig("plots/" + region + "_FullBreakdown_IT.png")

  df_breakdown = df_region[["data", "terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
  ax = df_breakdown.set_index("data").plot.bar(stacked=True)
  ax.grid(axis="y")

  ax.set_title(region + " tests breakdown (excluding negatives)")
  ax.set_ylabel("# tests")
  ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths", "Negatives"])
  plt.savefig("plots/" + region + "_Breakdown_EN.png")

  ax.set_title("Casistica dei tamponi in " + region + " (eccetto negativi)")
  ax.set_ylabel("# tamponi")
  ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti", "Negativi"])
  plt.savefig("plots/" + region + "_Breakdown_IT.png")

  df_relative = df_region[["data","tamponi", "terapia_intensiva", "ricoverati_con_sintomi", "isolamento_domiciliare","dimessi_guariti", "deceduti"]]
  df_relative["terapia_intensiva"] = df_relative["terapia_intensiva"]/df_relative["tamponi"]
  df_relative["ricoverati_con_sintomi"] = df_relative["ricoverati_con_sintomi"]/df_relative["tamponi"]
  df_relative["isolamento_domiciliare"] = df_relative["isolamento_domiciliare"]/df_relative["tamponi"]
  df_relative["dimessi_guariti"] = df_relative["dimessi_guariti"]/df_relative["tamponi"]
  df_relative["deceduti"] = df_relative["deceduti"]/df_relative["tamponi"]
  df_relative = df_relative.drop("tamponi", 1)
  ax = df_relative.set_index("data").plot.bar(stacked=True)
  ax.grid(axis="y")

  ax.set_title(region + " tests breakdown relative to total number of tests")
  ax.set_ylabel("Fraction w.r.t. total tests")
  ax.legend(["ICU cases", "Hospitalised w/ symptoms", "Quarantined at home", "Recoveries", "Deaths"])
  plt.savefig("plots/" + region + "_Breakdown_Relative_EN.png")
  
  ax.set_title("Casistica percentuale dei tamponi in " + region)
  ax.set_ylabel("Frazione dei tamponi totali")
  ax.legend(["Terapia intensiva", "Ricoverati con sintomi", "Isolamento domiciliare", "Guariti", "Morti"])
  plt.savefig("plots/" + region + "_Breakdown_Relative_IT.png")
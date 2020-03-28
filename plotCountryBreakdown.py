import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np
import os
import matplotlib.dates as mdates
from JohnHopkinsDataProvider import getJohnHopkinsCOVIDData


# tick on mondays every week

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Ensure a major tick for each week using (interval=1) 


countries = ["China", "Italy", "United Kingdom"]

df_merged = getJohnHopkinsCOVIDData(countries)

df_countries = [df_merged[df_merged["Country/Region"] == country] for country in countries]

for index, df_country in enumerate(df_countries):
  
  fig_country = plt.figure()
  ax_country = fig_country.add_subplot(1, 1, 1)

  country = countries[index]
  df_country = df_country.sort_values(by="date")
  df_country_selected = df_country[["date", "active", "recovered", "deaths"]]
  ax_country.bar(df_country_selected.date, df_country_selected.active)
  ax_country.bar(df_country_selected.date, df_country_selected.recovered, bottom=df_country_selected.active)
  ax_country.bar(df_country_selected.date, df_country_selected.deaths, bottom=df_country_selected.active+df_country_selected.recovered)
  
  ax_country.xaxis_date()
  ax_country.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
  ax_country.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
  ax_country.set_title("Test breakdown in " + country)
  ax_country.set_ylabel("# cases")
  ax_country.legend(["Active", "Recovered", "Deaths"], loc="upper left")
  ax_country.grid(axis="y")
  fig_country.savefig("plots/" + country.replace(" ", "") + "_Cases_EN.png")

  ax_country.set_title("Casi in " + country)
  ax_country.set_ylabel("# casi")
  ax_country.legend(["Positivi", "Guariti", "Morti"], loc="upper left")
  ax_country.grid(axis="y")
  fig_country.savefig("plots/" + country.replace(" ", "") + "_Cases_IT.png")


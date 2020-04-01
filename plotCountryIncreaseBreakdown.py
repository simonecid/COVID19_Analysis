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


# countries = ["Italy"]
countries = ["China", "Italy", "United Kingdom"]

df_countries = getJohnHopkinsCOVIDData(countries)

for index, df_country in enumerate(df_countries):
  
  fig_country = plt.figure()
  ax_country = fig_country.add_subplot(1, 1, 1)

  country = countries[index]
  df_country_selected = df_country[["date", "confirmed", "recovered", "deaths"]]
  df_country_selected["new_confirmed"] = df_country_selected["confirmed"].diff()
  df_country_selected["new_recovered"] = df_country_selected["recovered"].diff()
  df_country_selected["new_deaths"] = df_country_selected["deaths"].diff()
  ax_country.bar(df_country_selected.date[1:], df_country_selected["new_confirmed"][1:], color="tab:orange")
  ax_country.bar(df_country_selected.date[1:], -df_country_selected["new_recovered"][1:], color="tab:green" )
  ax_country.bar(df_country_selected.date[1:], -df_country_selected["new_deaths"][1:], bottom=(-df_country_selected["new_recovered"][1:]), color="tab:red")
  
  ax_country.xaxis_date()
  ax_country.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
  ax_country.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
  ax_country.set_title("Daily test breakdown in " + country)
  ax_country.set_ylabel("# cases")
  ax_country.legend(["New confirmed", "New recovered", "New deaths"], loc="upper left")
  ax_country.grid(axis="y")
  fig_country.savefig("plots/" + country.replace(" ", "") + "_DailyCases_EN.png")

  ax_country.set_title("Casi giornalieri in " + country)
  ax_country.set_ylabel("# casi")
  ax_country.legend(["Nuovi casi", "Nuovi guariti", "Nuovi morti"], loc="upper left")
  ax_country.grid(axis="y")
  fig_country.savefig("plots/" + country.replace(" ", "") + "_DailyCases_IT.png")


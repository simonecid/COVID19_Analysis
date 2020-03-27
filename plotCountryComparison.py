import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np
import os
import matplotlib.dates as mdates



# Ensure a major tick for each week using (interval=1) 


countries = ["China", "Italy", "United Kingdom"]

categories = ["active", "confirmed", "recovered"]

df_confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
df_confirmed = df_confirmed[df_confirmed["Country/Region"].isin(countries)]
df_confirmed_skimmed = df_confirmed.drop(["Lat", "Long"], 1)
df_confirmed_rearranged = pd.melt(df_confirmed_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="confirmed")

df_recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
df_recovered = df_recovered[df_recovered["Country/Region"].isin(countries)]
df_recovered_skimmed = df_recovered.drop(["Lat", "Long"], 1)
df_recovered_rearranged = pd.melt(df_recovered_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="recovered")

df_deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
df_deaths = df_deaths[df_deaths["Country/Region"].isin(countries)]
df_deaths_skimmed = df_deaths.drop(["Lat", "Long"], 1)
df_deaths_rearranged = pd.melt(df_deaths_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="deaths")

df_merged = df_confirmed_rearranged.merge(df_deaths_rearranged, how="outer").merge(df_recovered_rearranged, how="outer")
df_merged = df_merged.groupby(["date", "Country/Region"]).sum().reset_index()
df_merged["active"] = df_merged["confirmed"] - df_merged["recovered"] - df_merged["deaths"]
df_merged["date"] = pd.to_datetime(df_merged["date"])

df_countries = [df_merged[df_merged["Country/Region"] == country] for country in countries]


for category in categories:
  
  fig_category = plt.figure()
  ax_category = fig_category.add_subplot(1, 1, 1)
  
  for index, country in enumerate(countries):

    df_country = df_countries[index].sort_values(by="date")
    df_country_selected = df_country[["date", category]]
    ax_category.plot(df_country_selected.date, df_country_selected[category])
    
  ax_category.xaxis_date()
  ax_category.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
  ax_category.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
  ax_category.set_title("Number of " + category + " cases")
  ax_category.set_ylabel("# cases")
  ax_category.legend(countries, loc="upper left")
  ax_category.grid()
  fig_category.savefig("plots/Comparison_"+ category +"_Cases_EN.png")

  ax_category.set_title("Numero di casi " + category)
  ax_category.set_ylabel("# casi")
  ax_category.legend(countries, loc="upper left")
  ax_category.grid()
  fig_category.savefig("plots/Comparison_"+ category +"_Cases_IT.png")


import pandas as pd
import matplotlib.pyplot as plt
import sys
import dateutil
import numpy as np
import os
import matplotlib.dates as mdates
from JohnHopkinsDataProvider import getJohnHopkinsCOVIDData


# Ensure a major tick for each week using (interval=1) 


countries = ["China", "Italy", "United Kingdom"]

categories = ["active", "confirmed", "recovered"]

df_merged = getJohnHopkinsCOVIDData(countries)

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


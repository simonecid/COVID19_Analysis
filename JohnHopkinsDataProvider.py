import pandas as pd

def getJohnHopkinsCOVIDData(countries=None):
  df_confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
  if countries is not None: df_confirmed = df_confirmed[df_confirmed["Country/Region"].isin(countries)]
  df_confirmed_skimmed = df_confirmed.drop(["Lat", "Long"], 1)
  df_confirmed_rearranged = pd.melt(df_confirmed_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="confirmed")

  df_recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
  if countries is not None: df_recovered = df_recovered[df_recovered["Country/Region"].isin(countries)]
  df_recovered_skimmed = df_recovered.drop(["Lat", "Long"], 1)
  df_recovered_rearranged = pd.melt(df_recovered_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="recovered")

  df_deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
  if countries is not None: df_deaths = df_deaths[df_deaths["Country/Region"].isin(countries)]
  df_deaths_skimmed = df_deaths.drop(["Lat", "Long"], 1)
  df_deaths_rearranged = pd.melt(df_deaths_skimmed, id_vars=["Province/State", "Country/Region"], var_name="date", value_name="deaths")

  df_merged = df_confirmed_rearranged.merge(df_deaths_rearranged, how="outer").merge(df_recovered_rearranged, how="outer")
  df_merged = df_merged.groupby(["date", "Country/Region"]).sum().reset_index()
  df_merged["active"] = df_merged["confirmed"] - df_merged["recovered"] - df_merged["deaths"]
  df_merged["date"] = pd.to_datetime(df_merged["date"])

  # creating a list of country-level data frames sorted by date
  if countries is not None:
    df_countries = [df_merged[df_merged["Country/Region"] == country].sort_values(by="date") for country in countries]
  else: 
    df_countries = [df_merged.sort_values(by="date")]


  return df_countries
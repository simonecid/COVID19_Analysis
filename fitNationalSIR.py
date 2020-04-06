"""
Andrea Dal Molin 09/03/2020
Edited by Simone Bologna to fit more stuff
This script applies the SIR epidemic model to the COVID19 epidemic
https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
"""

# ---------- Imports ----------
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import datetime as dt
from JohnHopkinsDataProvider import getJohnHopkinsCOVIDData
import matplotlib.dates as mdates

class SIR:
  def __init__(self, infected, removed, days, **kwargs):
    self.infected = infected
    self.removed = removed
    self.days = days
    

  # ---------- Functions ----------
  def sir_model(self, y, x, beta, gamma):
      N, S, I, R  = y
      dS = -beta * S * I / N
      dR = gamma * I
      dI = -(dS + dR)
      return 0, dS, dI, dR


  def fit_odeint(self, x, beta, gamma, N, S0, I0, R0):
      return integrate.odeint(self.sir_model, (N, S0, I0, R0), x, args=(beta, gamma))[:,-2:].T.flatten()


  def chisquare(self, comb_data, fitted):
      return np.sum(((comb_data - fitted)**2)/comb_data)


  def optimal_SIR(self, N):
      # ---------- Initial parameters ----------
      I0 = self.infected[0]  # Infected population
      R0 = self.removed[0]   # Removed population (number of dead + number of recovered with immunity)
      S0 = N - I0 - R0  # Susceptible population

      # ---------- Fit parametes with current data ----------
      comb_data = np.append(self.infected, self.removed)
      fit =  lambda x, beta, gamma: self.fit_odeint(x, beta, gamma, N, S0, I0, R0)
      popt, pcov = optimize.curve_fit(fit, self.days, comb_data, bounds=(0, 1))
      fitted = self.fit_odeint(self.days, popt[0], popt[1], N, S0, I0, R0)
      chi2 = self.chisquare(comb_data, fitted)
      red_chi2 = chi2/(len(self.infected) + len(self.removed) - len(popt))
      return red_chi2

  def fit(self):
    # ---------- Find optimal N parameter ----------

    optimal_SIR =  lambda N: self.optimal_SIR(N)
    result =optimize.minimize(optimal_SIR, x0, method = 'Nelder-Mead')
    print(result)

    # ---------- Initial parameters ----------
    self.N = result.x      # Total population
    self.I0 = self.infected[0]  # Infected population
    self.R0 = self.removed[0]   # Removed population (number of dead + number of recovered with immunity)
    self.S0 = self.N - self.I0 - self.R0  # Susceptible population

    # ---------- Fit parametes with current data ----------
    comb_data = np.append(self.infected, self.removed)
    fit =  lambda x, beta, gamma: self.fit_odeint(x, beta, gamma, self.N, self.S0, self.I0, self.R0)
    popt, pcov = optimize.curve_fit(fit, self.days, comb_data, bounds=(0, 1))
    fitted = self.fit_odeint(self.days, popt[0], popt[1], self.N, self.S0, self.I0, self.R0)
    chi2 = self.chisquare(comb_data, fitted)
    red_chi2 = chi2/(len(self.infected) + len(self.removed) - len(popt))

    # ---------- Compute BRN ----------
    BRN = popt[0] / popt[1]  # Basic reproduction number
    BRN_err = BRN * np.sqrt((np.sqrt(pcov[0][0])/popt[0])**2 + (np.sqrt(pcov[1][1])/popt[1])**2)

    self.popt = popt
    self.pcov = pcov
    self.BRN = BRN
    self.BRN_err = BRN
    self.red_chi2 = red_chi2

  def find_epidemic_peak(self, ndays):
    # ---------- Extrapolate from model ----------
    t =  np.arange(0,ndays)
    model = integrate.odeint(self.sir_model, (self.N, self.S0, self.I0, self.R0), t, args=(self.popt[0], self.popt[1]))
    self.N, self.S, self.I, self.R = model.T

    # ---------- Find expected epidemic peak ----------
    y_max = np.amax(self.I)
    x_max = np.where(self.I == y_max)[0][0]
    return x_max, y_max
    

# ---------- Load data from csv ----------

countries = ["Italy", "France", "United Kingdom", "China"]
fit_ndays = [10, 20, 10, 10]
x0s = [100e3, 50e3, 100e3, 100e3]
# countries = ["Italy"]
# fit_ndays = [14,]
# x0s = [100e3]
nday_prediction = 140

df_countries = getJohnHopkinsCOVIDData(countries)

for index, (df, country, ndays, x0) in enumerate(zip(df_countries, countries, fit_ndays, x0s)):
  df = df[-ndays:]
  
  infected = np.array(df["active"])
  removed = np.array(df['recovered'] + df['deaths'])
  start_day = df.iloc[0]["date"]
  days = np.array((df["date"] - start_day)/np.timedelta64(1, "D"))
  x0 = np.array(x0)

  sir = SIR(infected=infected, removed=removed, days=days)
  sir.fit()

  N = sir.N
  popt = sir.popt
  pcov = sir.pcov
  BRN = sir.BRN
  BRN_err = sir.BRN_err
  red_chi2 = sir.red_chi2

  textstr = '\n'.join((
      r'$N=%.f$' % (N),
      r'$\beta=%.3f \pm %.3f$' % (popt[0], np.sqrt(pcov[0][0])),
      r'$\gamma=%.3f \pm %.3f$' % (popt[1], np.sqrt(pcov[1][1])),
      r'$R_0=%.2f \pm %.2f$' %  (BRN, BRN_err),
      r'$\chi_{red}^2=%.3f$' % (red_chi2)))


  x_max, y_max = sir.find_epidemic_peak(nday_prediction)

  peak_day = start_day + dt.timedelta(days = int(x_max)+1)
  peak_day_str = peak_day.strftime('%d-%m-%Y')

  # ---------- Plot results ----------
  fig = plt.figure(facecolor='w')
  ax = fig.add_subplot(111, axisbelow=True)

  t = np.arange(start_day, start_day+dt.timedelta(days=nday_prediction), dtype='datetime64[D]')

  plt.xticks(rotation=90)
  ax.xaxis_date()
  ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
  ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

  ax.plot(df["date"], infected, 'ro')
  ax.plot(df["date"], removed, 'gx')
  ax.plot(t, sir.S, 'b', alpha=0.5, lw=2)
  ax.plot(t, sir.I, 'r', alpha=0.5, lw=2)
  ax.plot(t, sir.R, 'g', alpha=0.5, lw=2)


  props = dict(boxstyle='round', edgecolor='0.7', facecolor='white', alpha=0.7)
  ax.text(0.676, 0.5, textstr, transform=ax.transAxes, fontsize=10,
          verticalalignment='top', bbox=props)
  ax.grid(b=True, which='major', ls='-')

  ax.set_title('COVID-19 - ' + country)
  ax.set_ylabel('Number of people')
  annotation = ax.annotate("EPIDEMIC PEAK\nInfected = " + str(int(y_max)) + "\non " + peak_day_str,
              xy=(mdates.date2num(peak_day), y_max), xycoords='data',
              xytext=(mdates.date2num(peak_day), y_max*1.2), textcoords='data',
              arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
              bbox=props
              )

  plt.legend([
      'Data on positives',
      'Data on removed',
      'Susceptible',
      'Infected',
      'Removed'
    ],
    loc=1, bbox_to_anchor=(1, 0.9))

  plt.savefig("plots/SIR_covid19_" + country.replace(" ", "") + "_EN.png")

  annotation.remove() 

  ax.set_ylabel('Numero di persone')
  annotation = ax.annotate("PICCO EPIDEMICO\nInfetti = " + str(int(y_max)) + "\nil " + peak_day_str,
              xy=(mdates.date2num(peak_day), y_max), xycoords='data',
              xytext=(mdates.date2num(peak_day), y_max*1.2), textcoords='data',
              arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
              bbox=props
              )

  plt.legend([
      'Dati sui positivi',
      'Dati sui rimossi',
      'Suscettibili',
      'Infetti',
      'Rimossi'
    ],
    loc=1, bbox_to_anchor=(1, 0.9))
  plt.savefig("plots/SIR_covid19_" + country.replace(" ", "") + "_IT.png")
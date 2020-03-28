"""
ADM 09/03/2020
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

# ---------- Functions ----------
def sir_model(y, x, beta, gamma):
    N, S, I, R  = y
    dS = -beta * S * I / N
    dR = gamma * I
    dI = -(dS + dR)
    return 0, dS, dI, dR


def fit_odeint(x, beta, gamma, N, S0, I0, R0):
    return integrate.odeint(sir_model, (N, S0, I0, R0), x, args=(beta, gamma))[:,-2:].T.flatten()


def chisquare(comb_data, fitted):
    return np.sum(((comb_data - fitted)**2)/comb_data)


def optimal_SIR(N):
    # ---------- Initial parameters ----------
    I0 = infected[0]  # Infected population
    R0 = removed[0]   # Removed population (number of dead + number of recovered with immunity)
    S0 = N - I0 - R0  # Susceptible population

    # ---------- Fit parametes with current data ----------
    comb_data = np.append(infected, removed)
    fit =  lambda x, beta, gamma: fit_odeint(x, beta, gamma, N, S0, I0, R0)
    popt, pcov = optimize.curve_fit(fit, days, comb_data, bounds=(0, 1))
    fitted = fit_odeint(days, popt[0], popt[1], N, S0, I0, R0)
    chi2 = chisquare(comb_data, fitted)
    red_chi2 = chi2/(len(infected) + len(removed) - len(popt))
    return red_chi2


# ---------- Load data from csv ----------

region = "Lombardia"

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
df_region = df[df["denominazione_regione"] == region]
infected = np.array(df_region["totale_attualmente_positivi"])
removed = np.array(df_region['dimessi_guariti'] + df_region['deceduti'])
days = np.arange(0, len(infected))

# ---------- Find optimal N parameter ----------
x0 = np.array([5e4])
result =optimize.minimize(optimal_SIR, x0, method = 'Nelder-Mead')
print(result)

# ---------- Initial parameters ----------
N = result.x      # Total population
I0 = infected[0]  # Infected population
R0 = removed[0]   # Removed population (number of dead + number of recovered with immunity)
S0 = N - I0 - R0  # Susceptible population

# ---------- Fit parametes with current data ----------
comb_data = np.append(infected, removed)
fit =  lambda x, beta, gamma: fit_odeint(x, beta, gamma, N, S0, I0, R0)
popt, pcov = optimize.curve_fit(fit, days, comb_data, bounds=(0, 1))
fitted = fit_odeint(days, popt[0], popt[1], N, S0, I0, R0)
chi2 = chisquare(comb_data, fitted)
red_chi2 = chi2/(len(infected) + len(removed) - len(popt))

# ---------- Compute BRN ----------
BRN = popt[0] / popt[1]  # Basic reproduction number
BRN_err = BRN * np.sqrt((np.sqrt(pcov[0][0])/popt[0])**2 + (np.sqrt(pcov[1][1])/popt[1])**2)

textstr = '\n'.join((
    r'MODEL PARAMETERS:  ',
    r'$N=%.f$' % (N),
    r'$\beta=%.3f \pm %.3f$' % (popt[0], np.sqrt(pcov[0][0])),
    r'$\gamma=%.3f \pm %.3f$' % (popt[1], np.sqrt(pcov[1][1])),
    r'$R_0=%.2f \pm %.2f$' %  (BRN, BRN_err),
    r'$\chi_{red}^2=%.3f$' % (red_chi2)))

# ---------- Extrapolate from model ----------
t =  np.arange(0,140)
model = integrate.odeint(sir_model, (N, S0, I0, R0), t, args=(popt[0], popt[1]))
N, S, I, R = model.T

# ---------- Find expected epidemic peak ----------
y_max = np.amax(I)
x_max = np.where(I == y_max)[0][0]
start_day = dt.date(2020, 2, 24)
peak_day = start_day + dt.timedelta(days = int(x_max)+1)
peak_day = peak_day.strftime('%d-%m-%Y')

# ---------- Plot results ----------
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)

ax.plot(days, infected, 'ro', label='Data on positives')
ax.plot(days, removed, 'gx', label='Data on removed')

ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Removed')

ax.set_title('COVID-19 - ' + region)
ax.set_xlabel('Number of days starting from Fabruary 24th 2020')
ax.set_ylabel('Number of people')

props = dict(boxstyle='round', edgecolor='0.7', facecolor='white', alpha=0.7)
ax.text(0.676, 0.5, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

ax.annotate("EPIDEMIC PEAK\nInfected = " + str(int(y_max)) + "\non " + peak_day,
            xy=(x_max, y_max), xycoords='data',
            xytext=(x_max*1.2, y_max*1.2), textcoords='data',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
            bbox=props
            )

ax.grid(b=True, which='major', ls='-')
plt.legend(loc=1, bbox_to_anchor=(1, 0.9))

plt.tight_layout()

plt.savefig("SIR_covid19.png")
plt.show()

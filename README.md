**English version down below.**

# Grafici COVID 19

Estrae automaticamente dati del COVID19 dal repository ufficiale della [Protezione Civile](https://github.com/pcm-dpc/COVID-19) e [John Hopkins](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data) e crea dei grafici.

[I grafici piu' recenti sono disponibili sulla wiki; si aggiorna automaticamente ogni giorno alle 20, ora italiana.](https://github.com/simonecid/COVID19_Analysis/wiki)

# COVID 19 Plotting tools

Automatically pulls COVID19 data from the official [Italian](https://github.com/pcm-dpc/COVID-19) and [John Hopkins](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data) repository and plots it.

[Latest plots are available on the Wiki; updates daily at 8PM, Rome time.](https://github.com/simonecid/COVID19_Analysis/wiki)

## Usage

Requires Pandas, Numpy and Matplotlib to be installed.

Run 

 * ```plotRegionBreakdown.py``` to plot and save to file breakdowns of the tests in specific Italian regions. You can set the regions by editing the regions list at the beginning of the script.
 * ```plotItalianBreakdown.py``` to plot and save to file breakdowns of the tests in Italy.
 * ```plotProvinceData.py``` to plot the number of total cases in specific Italian provinces over time. You can set the provinces by editing the list at the beginning of the script.

The breakdown scripts produce three plot types in both English and Italian:

 1) Breakdown of tests as a stacked plot in six categories: ICU cases, Hospitalised cases, Quarantined cases, Recoveries, Deaths, Negatives
 2) Same as 1), but without negatives
 3) Same as 2), but the number in each category is divided by the total number of test by that day, displaying the relative fraction of tests falling in each category.

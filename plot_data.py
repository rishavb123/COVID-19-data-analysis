import numpy as np
import matplotlib.pyplot as plt

from plots import plot_time_series_data
from transforms import *

files = [
    "./data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "./data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "./data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
]
names = [
    "Global Confirmed Cases",
    "Global Death Cases",
    "Global Recovered Case"
]

country = "Italy"

# plot_time_series_data(files, names, country=country)
# plot_time_series_data(files, names, np.log, "Log(Cases)", country=country)
plot_time_series_data(files, names, composite([integral]), "\int(Cases)*d(Days)", country=country, best_fit_degree=2)
# plot_time_series_data(files, names, composite([derivative, smooth]), "d(Cases)/d(Days)", country=country)
# plot_time_series_data(files, names, composite([derivative, smooth, derivative, remove_outliers]), "d^2(Cases)/d(Days)^2", country=country)


plt.show()
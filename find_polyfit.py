import matplotlib.pyplot as plt

from plots import plot_time_series_data_from_file
from rb_math.transforms import *

files = [
    "./data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
]
names = [
    "Global Confirmed Cases"
]

country = None
max_best_fit_degree = 15
threshold = 1e-2
show = True
import sys
transform = composite((sub(0, int(sys.argv[1])), remove_outliers))

last_mse = 0
orig_mse = 0

for best_fit_degree in range(1, max_best_fit_degree):
    p, mse = plot_time_series_data_from_file(files, names, country=country, transform=transform, best_fit_degree=best_fit_degree)
    print("Best Fit Degree:", best_fit_degree)
    print("Weights:", p)
    print("Mean Squared Error:", mse)
    if best_fit_degree != 1:
        r = (last_mse - mse) / orig_mse
        print("Improvement:", r)
        if r < threshold: break
    else:
        orig_mse = mse
    last_mse = mse
    print()

if show:
    plt.show()
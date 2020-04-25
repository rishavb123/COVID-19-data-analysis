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

# graph xs and ys (gxs, gys)
gxs = list(range(2,90))
gys = []
for gx in gxs:
    transform = composite((sub(0, gx), remove_outliers))

    last_mse = 0
    orig_mse = 0

    for best_fit_degree in range(1, max_best_fit_degree):
        p, mse = plot_time_series_data_from_file(files, names, country=country, transform=transform, best_fit_degree=best_fit_degree)
        plt.close()
        if best_fit_degree != 1:
            r = (last_mse - mse) / orig_mse
            if r < threshold: 
                gys.append(best_fit_degree - 1)
                break
        else:
            orig_mse = mse
        last_mse = mse

plt.scatter(gxs, gys,s=6)
p = np.polyfit(gxs[:50], gys[:50], 1)
plt.plot(gxs, [p[0] * x + p[1] for x in gxs])
plt.show()
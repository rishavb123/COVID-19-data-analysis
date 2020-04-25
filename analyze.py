import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from data import get_structured_data
from rb_math.transforms import *

data = get_structured_data()

countries = ["Global", "United States", "Spain"]#, "Italy", "France", "China", "India"]
# countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

backend = matplotlib.get_backend()

for country in countries:
    print("Beginning Analysis on " + country + " Data")
    s = (2, 3)
    fig, axs = plt.subplots(s[0], s[1])
    fig.canvas.set_window_title(country + " Analysis")
    d = data[country]
    transforms = (None, safe_log, composite([ratios, remove_outliers]), composite([growth_rate, remove_outliers]), composite([growth_rate, remove_outliers, derivative]))
    names = (None, 'logarithm', 'ratios', 'growth rate', 'growth rate derivative')

    def plot(data, name, transform_name, r, c):
        if transform_name != None:
            axs[r][c].plot(data, label=(name + ' ' + transform_name).title() + " in " + country)
        else:
            axs[r][c].plot(data, label=name.title() + " in " + country)
        axs[r][c].set_xlabel("Days after January 22, 2020")
        if transform_name != None:
            axs[r][c].set_ylabel(transform_name.title() + ' Cases')
        else:
            axs[r][c].set_ylabel('Cases')

    def plot_with_tranforms(data, name, transforms, names):
        for i in range(len(transforms)):
            t = transforms[i]
            if t == None:
                plot(data, name, names[i], int(i / s[1]), i % s[1])
            else:
                plot(t(data), name, names[i], int(i / s[1]), i % s[1])
    
    for name in d:
        plot_with_tranforms(d[name], name, transforms, names)
    if 'recovered' in d:
        plot_with_tranforms(d['death'] + d['recovered'], '(death + recovered)', transforms, names)

    manager = plt.get_current_fig_manager()

    if backend == 'TkAgg':
        manager.resize(*manager.window.maxsize())
    elif backend == 'wxAgg':
        manager.frame.Maximize(True)
    elif backend == 'Qt4Agg':
        manager.window.showMaximized()

    for ax in axs:
        for a in ax:
            a.legend()

    plt.show()

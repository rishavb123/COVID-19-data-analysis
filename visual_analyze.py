import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from data import get_structured_data
from rb_math.transforms import *

data = get_structured_data()

countries = [s.title() for s in sys.argv[1:]]
if len(countries) == 0 or countries[0] == "Default":
    countries = countries = ["Global", "United States", "Spain", "Italy", "France", "China", "India"]
elif countries[0] == "Test":
    countries = ["Global", "United States", "Spain"]
elif countries[0] == "Input":
    countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

for country in countries:
    print("Beginning Analysis on " + country + " Data")
    s = (2, 3)
    fig_name = country + " Analysis"
    fig, axs = plt.subplots(s[0], s[1], num=fig_name)
    # fig.canvas.set_window_title(fig_name)
    # plt.figure(fig_name)
    d = data[country]
    transforms = (None, safe_log, composite([derivative, remove_outliers]), composite([ratios, remove_outliers]), composite([growth_rate, remove_outliers]), composite([growth_rate, remove_outliers, derivative, remove_outliers, remove_outliers]))
    names = (None, 'logarithm', 'derivative', 'ratios', 'growth rate', 'growth rate derivative')
    use = (None, None, None, ["cases", "death"], ["cases"], ["cases"])
    polyfit_degree = (0, 0, 4, 0, 4, 4)

    def plot(data, name, transform_name, r, c):
        ind = names.index(transform_name)
        if use[ind] == None or name in use[ind]:
            if transform_name != None:
                axs[r][c].plot(data, label=(name + ' ' + transform_name).title() + " in " + country)
            else:
                axs[r][c].plot(data, label=name.title() + " in " + country)
            best_fit_degree = polyfit_degree[ind]
            if best_fit_degree > 0:
                p = np.polyfit(list(range(len(data))), data, best_fit_degree)
                bf_ys = [sum([(i ** j) * p[best_fit_degree - j] for j in range(best_fit_degree + 1)]) for i in range(len(data))]
                mse = np.mean(np.square(np.subtract(bf_ys, data)))
                axs[r][c].plot(bf_ys)
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

    fig.set_size_inches(19, 10)

    for ax in axs:
        for a in ax:
            leg = a.legend(fancybox=False, shadow=False)
            leg.get_frame().set_alpha(0.4)

    p = "res/imgs/plots/" + country.lower().replace(" ", "_")
    if not os.path.exists(p):
        os.mkdir(p)
    fig.savefig(p + "/analyze.png", bbox_inches='tight')  

    plt.show()
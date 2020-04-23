import matplotlib.pyplot as plt
import numpy as np

from transforms import *

def plot_time_series_data(files, names, transform=lambda ys: ys, ylabel=None, country=None, best_fit_degree=0):
    plt.figure()

    for filename, name in zip(files, names):
        f = open(filename)
        lines = f.readlines()
        ys = [0 for _ in lines[0].split(',')[3:]]
        for line in lines[1:]:
            l = line.split(',')
            if country == None or l[1].lower() == country.lower():
                l = l[3:]
                for i in range(len(ys)):
                    ys[i] += float(l[i])
        f.close()
        ys = transform(ys)
        plt.plot(ys, label=name)
        p, mse = None, None
        if best_fit_degree > 0:
            p = np.polyfit(list(range(len(ys))), ys, best_fit_degree)
            bf_ys = [sum([(i ** j) * p[best_fit_degree - j] for j in range(best_fit_degree + 1)]) for i in range(len(ys))]
            mse = np.mean(np.square(np.subtract(bf_ys, ys)))
            plt.plot(bf_ys, label=name + " Polyfit")

    plt.xlabel("Days after January 22, 2020")
    if ylabel is None:
        plt.ylabel("Cases for " + country if country != None else "Earth")
    else:
        plt.ylabel(ylabel + " for " + country if country != None else "Earth")
    plt.legend()

    return p, mse
import matplotlib.pyplot as plt
import numpy as np

from rb_math.transforms import *
from data import read

def plot_time_series_data_from_file(files, names, transform=None, ylabel=None, country=None, best_fit_degree=0, scatter=False, size=10, usa=False):
    plt.figure()
    if transform is None: transform = lambda ys: ys
    sp = smse = 0
    for filename, name in zip(files, names):
        ys = transform(read(filename, country=country, usa=usa))
        p, mse = plot_time_series_data(name, ys, scatter=scatter, size=size, best_fit_degree=best_fit_degree)
        if p is not None:
            sp += p
            smse += mse
    plt.xlabel("Days after January 22, 2020")
    c = (country if country != None else "Earth")
    if usa: c = "United States"
    if ylabel is None:
        plt.ylabel("Cases for " + c)
    else:
        plt.ylabel(ylabel + " for " + c)
    plt.legend()

    return sp, smse

def plot_time_series_data(name, ys, scatter=False, size=10, best_fit_degree=0):
    if scatter:
        plt.scatter(range(len(ys)), ys, label=name, s=size)
    else:
        plt.plot(ys, label=name)
    p, mse = None, None
    if best_fit_degree > 0:
        p = np.polyfit(list(range(len(ys))), ys, best_fit_degree)
        bf_ys = [sum([(i ** j) * p[best_fit_degree - j] for j in range(best_fit_degree + 1)]) for i in range(len(ys))]
        mse = np.mean(np.square(np.subtract(bf_ys, ys)))
        plt.plot(bf_ys, label=name + " Polyfit")
    return p, mse
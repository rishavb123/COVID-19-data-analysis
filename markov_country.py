import sys

import numpy as np
import matplotlib.pyplot as plt

from data import get_structured_data
from rb_math.transforms import *


# countries = [s.title() for s in sys.argv[1:]]
# if len(countries) == 0 or countries[0] == "Default":
#     countries = countries = ["Global", "United States", "Spain", "Italy", "France", "China", "India"]
# elif countries[0] == "Test":
#     countries = ["Global", "United States", "Spain"]
# elif countries[0] == "Input":
#     countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

countries = ['China', 'India', 'United States']
populations = {
    'China': 1.393e9,
    'India': 1.353e9,
    'United States': 328.2e6
}

data = get_structured_data()
for country in countries:
    cases = data[country]["cases"]
    deaths = data[country]["death"]
    plt.figure()
    rs = []
    r_ds = []
    r_rs = []
    s_is = []
    for i in range(len(cases) - 1):
        n_d = deaths[i + 1]
        n_e = 0
        n_n = cases[i + 1] - n_d - n_e
        n_p = populations[country] - n_n

        d = deaths[i]
        e = 0
        n = cases[i] - d - e
        p = populations[country] - n

        A = np.array([
            [n, 0, 0, p],
            [0, n, 0, 0],
            [0, 0, n, 0],
            [n, 0, 0, 0]
        ])
        b = np.array([n_n, n_d - d, n_e - e, n + p - n_p])

        if n != 0:

            r_d = (n_d - d) / n
            r_r = (n_e - e) / n
            r = (n + p - n_p) / n
            s_i = (n_n - n * r) / p

            rs.append(r)
            r_ds.append(r_d)
            r_rs.append(r_r)
            s_is.append(s_i)

    r = np.mean(rs)
    r_d = np.mean(r_ds)
    r_r = np.mean(r_rs)
    w = np.polyfit(list(range(len(s_is))), s_is, deg = 4)

    s = lambda i: sum([w[len(w) - 1 - j] * i ** j for j in range(len(w))])

    plt.scatter(list(range(len(s_is))), s_is)
    plt.plot(list(range(len(s_is))), [s(i) for i in range(len(s_is))])
    plt.show()

    T = lambda i: np.array([
        [r, 0, 0, s(i)],
        [r_d, 1, 0, 0],
        [r_r, 0, 1, 0],
        [1 - r, 0, 0, 1]
    ])

    print("r:", r, "r_d:", r_d, "r_r:", r_r)
    
    plt.plot(cases, label="Cases")
    pred = []
    counter = 0
    for i in range(0, int(len(cases) * 1)):
        if i >= len(cases) or cases[i] > 0:
            if len(pred) == 0:
                d = deaths[i]
                e = 0
                n = cases[i] - d - e
                p = populations[country] - n
                pred.append(np.array([n, d, e, p]))
            else:
                pred.append(np.matmul(T(i), pred[-1]))
        else: counter += 1
    plt.plot(list(range(counter, len(pred) + counter)), [t[0] for t in pred], label="Markov Chain")
    plt.figure()
    plt.plot(deaths, label="Deaths")
    plt.plot(list(range(counter, len(pred) + counter)), [t[1] for t in pred], label="Markov Chain")
    plt.legend()
    plt.show()
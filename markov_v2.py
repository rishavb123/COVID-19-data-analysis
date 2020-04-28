import matplotlib.pyplot as plt
import csv
import numpy as np

from rb_math.transforms import *

counties = ['Maricopa']
cases = {}
deaths = {}
populations = {}

with open('./data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv') as f:
    reader = csv.reader(f)
    fields = next(reader)
    for row in reader:
        county = row[fields.index("Admin2")]
        cases[county] = [int(s) for s in row[fields.index("1/22/20"):]]

with open('./data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv') as f:
    reader = csv.reader(f)
    fields = next(reader)
    for row in reader:
        county = row[fields.index("Admin2")]
        deaths[county] = [int(s) for s in row[fields.index("1/22/20"):]]
        populations[county] = int(row[fields.index("Population")])


for county in counties:
    rs = []
    r_ds = []
    r_rs = []
    ss = []
    plt.figure()
    for i in range(len(cases[county]) - 1):
        n_d = deaths[county][i + 1]
        n_e = 0
        n_n = cases[county][i + 1] - n_d - n_e
        n_p = populations[county] - n_n

        d = deaths[county][i]
        e = 0
        n = cases[county][i] - d - e
        p = populations[county] - n

        if n != 0:

            r_d = (n_d - d) / n
            r_r = (n_e - e) / n
            r = n_n / n

            rs.append(r)
            r_ds.append(r_d)
            r_rs.append(r_r)

    r = np.mean(rs)

    for i in range(len(cases[county]) - 1):
        n_d = deaths[county][i + 1]
        n_e = 0
        n_n = cases[county][i + 1] - n_d - n_e
        n_p = populations[county] - n_n

        d = deaths[county][i]
        e = 0
        n = cases[county][i] - d - e
        p = populations[county] - n

        if n != 0:

            ss.append((n_n - r * n) * populations[county] / n ** 2)

    r_d = np.mean(r_ds)
    r_r = np.mean(r_rs)
    plt.plot(ss)
    plt.show()

    do = True
    s = np.mean([s for s in ss if s != 0]) if do else 0
    # s/=1400

    T = np.array([
        [r, 0, 0, s],
        [r_d, 1, 0, 0],
        [r_r, 0, 1, 0],
        [0, 0, 0, 0]
    ])

    print(T)
    print("r:", r, "r_d:", r_d, "r_r:", r_r, "s: ", s, '-1/s:', -1/s)
    
    plt.plot(cases[county], label="Cases")
    pred = []
    counter = 0
    for i in range(0, int(len(cases[county]) * 1)):
        if i >= len(cases[county]) or cases[county][i] > 0:
            if len(pred) == 0:
                d = deaths[county][i]
                e = 0
                n = cases[county][i] - d - e
                p = n ** 2 / populations[county]
                pred.append(np.array([n, d, e, p]))
            else:
                state_vec = np.matmul(T, pred[-1])
                state_vec[3] = state_vec[0] ** 2 / populations[county]
                pred.append(state_vec)
        else: counter += 1
    plt.plot(list(range(counter, len(pred) + counter)), [t[0] for t in pred], label="Markov Chain")
    plt.figure()
    plt.plot(deaths[county], label="Deaths")
    plt.plot(list(range(counter, len(pred) + counter)), [t[1] for t in pred], label="Markov Chain")
plt.legend()
plt.show()
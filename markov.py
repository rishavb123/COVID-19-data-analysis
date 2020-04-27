import matplotlib.pyplot as plt
import csv
import numpy as np

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
    s_is = []
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
        [0, 0, 0, 0]
    ])

    print("r:", r, "r_d:", r_d, "r_r:", r_r)
    
    plt.plot(cases[county], label="Cases")
    pred = []
    counter = 0
    for i in range(0, int(len(cases[county]) * 1)):
        if i >= len(cases[county]) or cases[county][i] > 0:
            if len(pred) == 0:
                d = deaths[county][i]
                e = 0
                n = cases[county][i] - d - e
                p = populations[county] - n
                pred.append(np.array([n, d, e, p]))
            else:
                pred.append(np.matmul(T(i), pred[-1]))
        else: counter += 1
    plt.plot(list(range(counter, len(pred) + counter)), [t[0] for t in pred], label="Markov Chain")
    plt.figure()
    plt.plot(deaths[county], label="Deaths")
    plt.plot(list(range(counter, len(pred) + counter)), [t[1] for t in pred], label="Markov Chain")
plt.legend()
plt.show()
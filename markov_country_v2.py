import matplotlib.pyplot as plt
import csv
import numpy as np

from data import get_structured_data

# countries = [s.title() for s in sys.argv[1:]]
# if len(countries) == 0 or countries[0] == "Default":
#     countries = countries = ["Global", "United States", "Spain", "Italy", "France", "China", "India"]
# elif countries[0] == "Test":
#     countries = ["Global", "United States", "Spain"]
# elif countries[0] == "Input":
#     countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

countries = ['China']#, 'India', 'United States']
populations = {
    'China': 1.393e9,
    'India': 1.353e9,
    'United States': 328.2e6
}

data = get_structured_data()
for country in countries:
    cases = data[country]["cases"]
    deaths = data[country]["death"]
    recovered = data[country]["recovered"] if 'recovered' in data[country] else np.zeros_like(deaths)
    rs = []
    r_ds = []
    r_rs = []
    ss = []
    plt.figure()
    for i in range(len(cases) - 1):
        n_d = deaths[i + 1]
        n_e = 0
        n_n = cases[i + 1] - n_d - n_e
        n_p = populations[country] - n_n

        d = deaths[i]
        e = 0
        n = cases[i] - d - e
        p = populations[country] - n

        if n != 0:

            r_d = (n_d - d) / n
            r_r = (n_e - e) / n
            r = (n + p - n_p) / n

            rs.append(r)
            r_ds.append(r_d)
            r_rs.append(r_r)

    r = np.mean(rs)

    for i in range(len(cases) - 1):
        n_d = deaths[i + 1]
        n_e = 0
        n_n = cases[i + 1] - n_d - n_e
        n_p = populations[country] - n_n

        d = deaths[i]
        e = 0
        n = cases[i] - d - e
        p = populations[country] - n

        if n != 0:

            ss.append((n_n - r * n) * populations[country] / n ** 2)

    r_d = np.mean(r_ds)
    r_r = np.mean(r_rs)
    plt.plot(ss)
    plt.show()

    do = True
    s = np.mean(ss) if do else 0
    # s/=1400

    T = np.array([
        [r, 0, 0, s],
        [r_d, 1, 0, 0],
        [r_r, 0, 1, 0],
        [0, 0, 0, 0]
    ])

    print(T)
    print("r:", r, "r_d:", r_d, "r_r:", r_r, "s: ", s, '-1/s:', -1/s)
    
    plt.plot(cases, label="Cases")
    pred = []
    counter = 0
    for i in range(0, int(len(cases) * 1)):
        if i >= len(cases) or cases[i] > 0:
            if len(pred) == 0:
                d = deaths[i]
                e = 0
                n = cases[i] - d - e
                p = n ** 2 / populations[country]
                pred.append(np.array([n, d, e, p]))
            else:
                state_vec = np.matmul(T, pred[-1])
                state_vec[3] = state_vec[0] ** 2 / populations[country]
                pred.append(state_vec)
        else: counter += 1
    plt.plot(list(range(counter, len(pred) + counter)), [t[0] for t in pred], label="Markov Chain")
    plt.figure()
    plt.plot(deaths, label="Deaths")
    plt.plot(list(range(counter, len(pred) + counter)), [t[1] for t in pred], label="Markov Chain")
plt.legend()
plt.show()
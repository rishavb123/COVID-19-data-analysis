import sys

import numpy as np
import matplotlib.pyplot as plt

from data import get_structured_data
from rb_math.transforms import *


countries = [s.title() for s in sys.argv[1:]]
if len(countries) == 0 or countries[0] == "Default":
    countries = countries = ["Global", "United States", "Spain", "Italy", "France", "China", "India"]
elif countries[0] == "Test":
    countries = ["Global", "United States", "Spain"]
elif countries[0] == "Input":
    countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

data = get_structured_data()
for country in countries:

    print("Finding Differential Equation Parameters for " + country)

    N = np.array([d for d in data[country]["cases"] if d > 10])
    dNdi = np.array(remove_outliers(derivative(N)))
    N = N[:len(dNdi)]

    plt.plot(N)
    plt.figure()
    plt.plot(dNdi)
    plt.show()

    split_point = int(input("Enter the split point: "))
    c = np.mean((dNdi[:split_point]/N[:split_point]))
    print("c:", c)

    plt.plot(dNdi)
    plt.plot(N * c)
    plt.show()

    lim_val = max([(n - d/c) for n, d in zip(N[split_point:], dNdi[split_point:])])
    print("N^X:", lim_val)

    plt.plot(dNdi)
    plt.plot(c * (1 - N / lim_val) * N)
    plt.figure()
    plt.plot([0, len(N)], [lim_val, lim_val])
    plt.plot(N)
    plt.show()
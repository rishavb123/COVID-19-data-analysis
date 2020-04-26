import sys

import numpy as np
import matplotlib.pyplot as plt
import pprint

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
show = False

vals = []

for country in countries:
    d = data[country]["cases"]
    ind = 0
    for ind in range(len(d)):
        if d[ind] > 10: break
    d = np.array(safe_log(d[ind:]))
    p = np.polyfit(list(range(len(d))), d, 1)
    def f(x):
        return p[0] * x + p[1]
    if show:
        plt.plot(d)
        plt.plot([0, len(d) - 1], [f(0), f(len(d) - 1)])
        plt.show()
    r_squared = np.linalg.norm(d - np.vectorize(f)(list(range(len(d))))) ** 2 / np.linalg.norm(d - np.mean(d)) ** 2
    vals.append((country, r_squared))

vals.sort(key=lambda x: x[1], reverse=True)
for v in vals:
    print(v[0] + ":", v[1])
import numpy as np
import matplotlib.pyplot as plt

from data import get_structured_data
from rb_math.transforms import *

data = get_structured_data()
country = "Global"
N = np.array(data["Global"]["cases"])
dNdi = np.array(derivative(N))

split_point = 60
c = np.mean((dNdi[:split_point]/N[:split_point]))
print(c)
plt.plot(N)
plt.figure()
plt.plot(dNdi)
plt.plot(N * c)
plt.show()
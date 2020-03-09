import matplotlib.pyplot as plt
import numpy as np


f = open('./data.csv')
data = [int(x) for x in f.readlines()[1].split(',')[3:]]
f.close()

plt.plot(data)
plt.show()
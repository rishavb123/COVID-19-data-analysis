import numpy as np
import matplotlib.pyplot as plt

def plot(f, start, end, n=100):
    xs = np.arange(start, end, (end - start) / n)
    ys = [f(x) for x in xs]
    plt.plot(xs, ys)
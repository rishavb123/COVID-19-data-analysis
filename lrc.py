import numpy as np
import matplotlib.pyplot as plt

start = 0
end = 25000
N = 10000
h = (end - start) / N

I0 = 0
Q0 = 0

Vb = lambda t: 1 - np.exp(-10 * (t + 1)/(end - start))
L = lambda t: 100000
C = lambda t: 150
R = lambda t: 50

def f(x, t):
    A = np.array([
        [0, 1],
        [-1/(L(t)*C(t)), -R(t)/L(t)]
    ])
    b = np.array([0, Vb(t)])
    return np.matmul(A, x) + b

ts = np.arange(start, end, h)
Qs = []
Is = []

x = np.array([Q0, I0], float)

for t in ts:
    Qs.append(x[0])
    Is.append(x[1])

    k1 = h * f(x, t)
    k2 = h * f(x + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(x + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(x + k3, t + h)
    x += (k1 + 2 * k2 + 2 * k3 + k4) / 6

plt.plot(ts, Qs, label="Q", color='blue')
plt.plot(ts, [C(t) * L(t) * Vb(t) for t in ts], label="approaching", color='purple')
plt.plot([start, end], [0,0], color='black')
plt.legend()

plt.figure()
plt.plot(ts, Is, label="I", color='green')
plt.plot([start, end], [0,0], color='black')
plt.legend()

plt.figure()
plt.plot(ts[1:], [Is[i + 1] - Is[i] for i in range(len(Is) - 1)], label="\delta I", color='green')
plt.plot([start, end], [0,0], color='black')
plt.legend()

plt.show()
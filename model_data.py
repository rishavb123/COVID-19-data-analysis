import numpy as np
import matplotlib.pyplot as plt

from rb_math.gradient_descent import Model
from rb_math.plot_func import plot
from data import read

filename = "./data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def f(x, theta):
    return np.dot([1, x], theta)

def f_gradient(theta, x):
    return np.array([1, x])

def loss(y_hat, y):
    return (y_hat - y) ** 2

def loss_derivative(y_hat, y):
    return 2 * (y_hat - y)

model = Model(f, np.random.random(2) * 2e6 - 1e6, f_gradient, loss, loss_derivative, alpha=0.000001, alpha_decay=0.99, regularization=False)
print(model.theta)
y = read(filename)
x = list(range(len(y)))
model.train(x, y, epoch=1, delay=False)
plt.scatter(x, y, color='blue', label='Data', s=10)
# plt.plot(x, model.predict(x), color='red', label='Regression Line')
plt.legend()
plt.figure()
# plot(lambda x: 1e6 / (1 + np.exp(-x * 0.03)), -len(y), len(y), label='Hard-Coded Function')
plot(lambda x: 2 ** (x * 0.01), -len(y)*5, len(y) * 5, label='Hard-Coded Function')
plt.legend()
plt.show()
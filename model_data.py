import numpy as np
import matplotlib.pyplot as plt

from rb_math.gradient_descent import Model
from rb_math.plot_func import plot
from data import read

filename = "./data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

def f(x, theta):
    y_0, T, r, c, x_s = theta
    return c * T * y_0 / (y_0 - (T - y_0) * np.exp(-r * (x - x_s)))

def weighted_f_gradient(gradient_weights):
    def f_gradient(theta, x):
        y_0, T, r, c, x_s = theta
        ert = np.exp(-r * (x - x_s))
        d =  (y_0 - (T - y_0) * ert)
        return np.array(gradient_weights) * np.array([
            c * d * T - T * y_0 * (1 + ert),
            c * d * y_0 + T * y_0 * ert,
            c * T * y_0 * (x * (y_0 - T) * ert),
            c * T * y_0 / (y_0 + (T - y_0) * np.exp(-r * x)),
            0
        ]) / d ** 2
    return f_gradient

def loss(y_hat, y):
    return (y_hat - y) ** 2

def loss_derivative(y_hat, y):
    return 2 * (y_hat - y)

# TODO: redo the model stuff and notes with proper math (change - to +)

theta_0 = np.array([
    1,#np.random.random() * 0.1,
    2e7, #6e6 + 2e6 * np.random.random(),
    0.12, #np.random.random() * 0.5
    5, #np.random.random() * 10
    0 # np.random.random() * 10
])
model = Model(f, theta_0, weighted_f_gradient([0, 1, 0, 0]), loss, loss_derivative, alpha=0.0000001, alpha_decay=0.99, regularization=False)
print(model.theta) 
y = read(filename)
x = list(range(len(y)))
model.train(x, y, epoch=5000, delay=False)
plt.scatter(x, y, color='blue', label='Data', s=10)
plt.plot(x, model.predict(x), color='red', label='Model Curve')
plt.legend()
plt.show()
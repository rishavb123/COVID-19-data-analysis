import matplotlib.pyplot as plt
import numpy as np
import sys
import time

def maximize(J, theta, gradients, iterations=1000, alpha=0.01, alpha_decay=1, log=True, regularization=False):
    return minimize(J, theta, lambda theta: -gradients(theta), iterations=iterations, alpha=alpha, alpha_decay=alpha_decay, log=log, regularization=regularization)

def minimize(J, theta, gradients, iterations=1000, alpha=0.01, alpha_decay=1, log=True, regularization=False):
    for epoch in range(1, 1 + iterations):
        if np.isnan(gradients(theta)[0]): 
            print()
            print("Gradient Descent diverged, consider lowering the learning rate")
            break
        grad = gradients(theta)
        if regularization:
            grad += 2 * theta
        theta -= alpha * grad
        alpha *= alpha_decay
        print("\tEpoch: {epoch: <20} J: {J: <20} Theta: {theta: <100}".format(epoch=(str(epoch)+"/" + str(iterations))[:20], J=str(J(theta))[:20], theta=str(theta)[:100]), end='\r')
    print()
    return J(theta)

class Model:

    def __init__(self, f, theta_0, f_gradient, loss, loss_derivative, alpha=0.01, alpha_decay=0.99, regularization=False):
        self.f = f
        self.theta = theta_0
        self.f_gradient = f_gradient
        self.loss = loss
        self.loss_derivative = loss_derivative
        self.params = self.theta
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.regularization = regularization

    def train(self, x, y, epoch=1000, log=True):
        assert len(x) == len(y)
        n = len(x)
        J = lambda theta: sum([loss(f(x[i], theta), y[i]) for i in range(n)])
        def gradients(theta):
            grads = []
            for t in range(len(theta)):
                grads.append(sum([self.loss_derivative(f(x[i], theta), y[i]) * self.f_gradient(theta, x[i])[t] for i in range(n)]))
            return np.array(grads)
        return minimize(J, self.theta, gradients, iterations=epoch, alpha=self.alpha, alpha_decay=self.alpha_decay, log=log, regularization=self.regularization)

    def predict(self, x):
        return np.array([self.f(xi, self.theta) for xi in x])

if __name__ == '__main__':
    
    print("---------------------------------Basic Gradient Descent Test---------------------------------")

    theta = np.array([2, 2], float)
    J = lambda theta: sum(np.square(theta)) + 2
    gradients = lambda theta: 2 * theta
    print(theta, J(theta), gradients(theta))
    minimize(J, theta, gradients)
    print(theta, J(theta), gradients(theta))


    print("\n\n---------------------------------Linear Regression Model Test---------------------------------")

    def f(x, theta):
        return np.dot([1, x], theta)

    def f_gradient(theta, x):
        return np.array([1, x])

    def loss(y_hat, y):
        return (y_hat - y) ** 2

    def loss_derivative(y_hat, y):
        return 2 * (y_hat - y)

    model = Model(f, np.random.random(2) * 4, f_gradient, loss, loss_derivative, alpha=0.01, alpha_decay=0.99, regularization=True)
    x = np.array([0, 1, 2, 3, 4, 5, 6, 10], float)
    y = np.array([2.9, 4.9, 7.2, 9.2, 11, 13, 14.8, 23.02], float) # 3 + 2 * x or theta = [3, 2]
    model.train(x, y, epoch=10000)
    plt.scatter(x, y, color='blue', label='Data')
    plt.plot(x, model.predict(x), color='red', label='Regression Line')
    plt.legend()
    plt.show()
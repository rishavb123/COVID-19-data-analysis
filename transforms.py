import numpy as np

def integral(ys):
    return [sum(ys[0:i]) for i in range(1, len(ys))]

def derivative(ys):
    dy = []
    for i in range(1, len(ys) - 1):
        dy.append((ys[i + 1] - ys[i - 1]) / 2)
    return dy

def second_derivative(ys):
    dy = []
    for i in range(1, len(ys) - 1):
        dy.append(ys[i + 1] + ys[i - 1] - 2 * ys[i])
    return dy

def growth_rate(ys):
    dy = second_derivative(ys)
    gs = []
    for i in range(1, len(dy)):
        gs.append(ys[i] / ys[i - 1])
    return gs

def smooth(ys, starting_point_ratio=0.3):
    c_points = np.fft.rfft(ys)
    c_points[int(starting_point_ratio * len(c_points)):] = 0
    return np.fft.irfft(c_points)

def smooth_with_custom_ratio(starting_point_ratio=0.3):
    return lambda ys: smooth(ys, starting_point_ratio=starting_point_ratio)

def composite(transforms):
    def transform(ys):
        for t in transforms:
            ys = t(ys)
        return ys
    return transform

def filter_y(f):
    return lambda ys: [y for y in ys if f(y)]

def remove_outliers(ys):
    mean = np.mean(ys)
    std = np.std(ys)
    return [y for y in ys if (mean - 2 * std < y < mean + 2 * std)]

def polyfit(best_fit_degree):
    def transform(ys):
        p = np.polyfit(list(range(len(ys))), ys, best_fit_degree)
        return [sum([(i ** j) * p[best_fit_degree - j] for j in range(best_fit_degree + 1)]) for i in range(len(ys))]
    return transform

def sub(start=None, end=None):
    return lambda ys: ys[start:end]
import sys

import tensorflow as tf

from data import get_structured_data

countries = [s.title() for s in sys.argv[1:]]
if len(countries) == 0 or countries[0] == "Default":
    countries = countries = ["Global", "United States", "Spain", "Italy", "France", "China", "India"]
elif countries[0] == "Test":
    countries = ["Global", "United States", "Spain"]
elif countries[0] == "Input":
    countries = [input("Enter a country:") for i in range(int(input("How many countries would you like to view:")))]

data = get_structured_data()
for country in countries:
    d = data[country]["cases"]

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(5, input_shape=(3, ), activation='relu'),
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dense(1, activation='relu')
    ])
    model.compile(optimizer='adam', loss='mse')
    xs = []
    ys = []
    for i in range(1, int(len(d))):
        xs.append([i, d[i - 1], d[i - 2]])
        ys.append(d[i])

    new_xs = []
    new_ys = list(d)
    for i in range(len(d), int(1.5 * len(d))):
        new_ys.append(model.predict([1, i, d[i - 1], d[i - 2]]))
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

k = 3.1668114e-6 # [Ha/K]
ef = 2.5
T1 = 50000
T2 = 75000
T3 = 100000
T4 = 200000
T5 = 300000

x = np.arange(0., 1.05, 0.05)
#f = 1 / (k * T1 * np.exp(-(x-ef)/(k * T1)))
#g = 1 / (k * T2 * np.exp(-(x-ef)/(k * T2)))
#h = 1 / (k * T3 * np.exp(-(x-ef)/(k * T3)))
#w = 1 / (k * T4 * np.exp(-(x-ef)/(k * T4)))
#r = 1 / (k * T5 * np.exp(-(x-ef)/(k * T5)))

f = b1*eta*np.exp(b1*x)*np.exp(eta)*np.exp(-eta*np.exp(b1*x))
g = b2*eta*np.exp(b2*x)*np.exp(eta)*np.exp(-eta*np.exp(b2*x))
h = b3*eta*np.exp(b3*x)*np.exp(eta)*np.exp(-eta*np.exp(b3*x))
w = b4*eta*np.exp(b4*x)*np.exp(eta)*np.exp(-eta*np.exp(b4*x))
r = b5*eta*np.exp(b5*x)*np.exp(eta)*np.exp(-eta*np.exp(b5*x))

#f = k*T1*np.log((1-x)/x)
#g = k*T2*np.log((1-x)/x)
#h = k*T3*np.log((1-x)/x)
#w = k*T4*np.log((1-x)/x)
#r = k*T5*np.log((1-x)/x)

# red dashes, blue squares and green triangles
plt.plot(x, f, 'k', x, g, 'r', x, h, 'b', x, w, 'g', x, r, 'y')
plt.show()

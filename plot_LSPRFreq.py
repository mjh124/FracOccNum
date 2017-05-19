#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Constants [and units]
elem_charge = 1.60217e-19 # [A*s]
m_eff = 1.9131e-31 # [kg] 0.21e
m_eff1 = 3.6437e-31 # [kg] 0.4e
m_eff2 = 9.1094e-31 # [kg] electron mass
#eps_0 = 8.8541878e-12 # [S4*A2*m-3*kg-1]
eps_0 = 8.8541878e-18 # [S4*A2*cm-3*kg-1]
eps_oo = 10 # unitless
eps_tol = 2.38 # unitless
gamma = 1e14 # [s-1]
conv = 3e17

# Generate function
x = np.linspace(1e20, 1e22, 200)
f = conv / np.sqrt(((x*elem_charge**2)/(m_eff*eps_0*(eps_oo+eps_tol)))-gamma**2)
g = conv / np.sqrt(((x*elem_charge**2)/(m_eff*eps_0*(eps_oo+eps_tol1)))-gamma**2)

# Plot
plt.plot(x, f, 'k', x, g, 'r')
plt.xlabel('Carrier Density [carriers/cm^3]')
plt.ylabel('Plamson Wavelength [nm]')
#plt.show()
plt.savefig('test.png', bbox_inches='tight')

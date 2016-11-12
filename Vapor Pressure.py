# Vapor pressure calculated from temperature
# Using the Antoine Equation

import math
#Constants A, B, C are defined
A = 8.07131
B = 1730.63
C = 233.426

T = range(1, 100)

#We define Antoine Equation
#Pressure is in torr
def anton(T1):
    return 10.000**(A - (B/(C + T1)))

P = [anton(i) for i in T]

#Plots the simulation
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(T, P, 'k-')
ax.set_xlabel('Temperature (C)')
ax.set_ylabel('Vapor Pressure (torr)')
plt.title('Vapor Pressure v. Temperature')
plt.show()

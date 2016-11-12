# Hyperloop valve capacity simulation as a function of angle
# WARNING: Results are quantized
# It is assumed that the radius of the valve is 2 inches, like the GVD-4
# Valve is closed at angle = 0, pi, 2*pi

import math
import random
import matplotlib.pyplot as plt

angle = input('Angle, in radians: ')
x = []
y = []
#Coordinates of the centre of the valve
Cx = 0
Cy = 0
cvx = []
cvy = []
#Edge of the metal seat
mex = []
mey = []
#Capacity
Cv = 0.0000
#Creates figure 1
plt.figure(1)

# X, Y coordinates
def xcordi(angle,r,centrex):
    return r*math.cos(angle) + centrex
def ycordi (angle,r,centrey):
    return r*math.sin(angle) + centrey

for q in range(0, 5000):
    rad = random.uniform(0, 2)
    alpha = random.uniform(0, 2*math.pi)
    theta = q*2*math.pi/5000
    #Semiaxis
    semx = 2*math.cos(angle)
    semy = 2
    # Coordinates of the valve edge
    cvx.append(xcordi(theta, 2, Cx))
    cvy.append(ycordi(theta, 2, Cy))
    mex.append(2*math.cos(theta)*abs(math.cos(angle)))
    mey.append(ycordi(theta, 2, Cy))

    x.append(xcordi(alpha, rad, Cx))
    y.append(ycordi(alpha, rad, Cy))
    #Checks if the point is inside the valve's cross-sectional area
    Check = ((x[q]**2)/(semx**2)) + ((y[q]**2)/(semy**2))
    if Check > 1:
        plt.plot(x[q], y[q], 'ro')
        Cv = Cv+1
    else:
        plt.plot(x[q], y[q], 'bs')

Cv = (Cv/q)*100 #Final capacity (%)
#Plots the simulation
plt.plot(cvx, cvy, 'k-', linewidth = 4.5)
plt.plot(mex, mey, 'g-', linewidth = 3.0)
plt.axis([-3, 3, -3, 3])
plt.title(('Cv = '+str(Cv)+' +-0.5%'))
plt.show()
print('Cv = '+str(Cv)+'%')
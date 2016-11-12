import math
import matplotlib.pyplot as plt

# The present simulation will be used to compute the power necessary to operate a thermal vacuum chamber
# Two different power settings will be used:
# Water
# Steam

# First, let's establish some constants
# All measurements are in SI units
P_reserve = 101300.00 #Pressure inside the reserve
P_atm = 101300.00 #Atmospheric Pressure
# Antoine equation constants
A = 8.07131
B = 1730.63
C = 233.426
# Defines a range
qq = range(1,20)
# Computes the overall set of possible temperatures
T = [5.00*pp for pp in qq]


# Set of pressures for the water
P_water = [0.8725, 1.2281, 1.7057, 2.3392, 3.1698, 4.2469, 5.6291, 7.3851, 9.5953, 12.352, 15.763, 19.947, 25.043,
                31.202, 38.597, 47.716, 57.868, 70.183, 84.609]
# Set of volumes of gas
v_i = [147.03, 106.32, 77.885, 57.762, 43.340, 32.879, 25.205, 19.515, 15.251, 12.026, 9.5639, 7.6670, 6.1935, 5.0396,
       4.1291, 3.4053, 2.8261, 2.3593, 1.9808]

# Enhalpy sets
h_water_in = [21.020, 42.022, 62.982, 83.915, 104.83, 125.74, 146.64, 167.53, 188.44, 209.34, 230.26, 251.18,
                     272.12, 293.07, 314.03, 335.02, 356.02, 377.04, 398.09]
h_water_res = 2514200 # Water in the reservoir tank1
h_steam_in = [2510.1, 2519.2, 2528.3, 2537.4, 2546.5, 2555.6, 2564.6, 2573.5, 2582.4, 2591.3, 2600.1, 2608.8, 2617.5,
              2626.1, 2634.6, 2643.0, 2651.4, 2659.6, 2667.6] # Steam in the vacuum chamber
h_steam_atm = 1000*2675.6 # Steam in the atmosphere, assuming 20 C and 1 atm

#Power outputs of pumps
w_pump = 78 #W
st_pump = 80 #W


#FUNCTIONS TIME

# Power, valid for both water and steam
def POW(h_in, h_out):
    return (h_out - 1000*h_in)

# Massflow out of the pumps
def massflow(Raw, h_in, h_out):
    return Raw/POW(h_in, h_out)


# Computes the quantities
POW_water = []
POW_steam = []
massflow_water = []
mass_flow_steam = []
for nn in range(0, 19):
    POW_water.append(POW(h_water_in[nn], h_water_res)) # Necessary power for liquid water
    POW_steam.append(POW(h_steam_in[nn], h_steam_atm)) # Necessary power for steam
    massflow_water.append(massflow(w_pump, h_water_in[nn], h_water_res)) # Actual water massflow
    mass_flow_steam.append(massflow(st_pump, h_steam_in[nn], h_steam_atm)) #Actual steam massflow



# Plots the outputs
fig = plt.figure(1)
# Power necessary to move 1 Kg of either water or steam
plt.subplot(211)
plt.plot(T, POW_water, 'b-') # Water
plt.plot(T, POW_steam, 'k-') # Steam
ax = fig.add_subplot(211)
ax.set_xlabel('Temperature (C)')
ax.set_ylabel('Power required (W/Kg)')
plt.title('Power necessary per Kg of fluid')
# Massflow that the pumps can actually move
plt.subplot(212)
plt.plot(T, massflow_water, 'b-') # Water
plt.plot(T, mass_flow_steam, 'k-') # Steam
ax = fig.add_subplot(212)
ax.set_xlabel('Temperature (C)')
ax.set_ylabel('Massflow (Kg/s)')
plt.yscale('logit') # Logarithmic scale on the y axis
plt.title('Actual pump discharge')

plt.show()
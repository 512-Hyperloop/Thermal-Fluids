# Fall 2016
# 512 Hyperloop documentation
# Redondo, Carlos; Quartermaster, leader of piping sub-team

"""
Heat transfer simulation of heat exchanger. It is designed to clarify possible issues that may arise if liquid
water is to be used as a coolant.

Equations are taking from the MIT website and Wikipedia
Prior assumptions:
    -Pipes will be idealized as 1 dimensional.
    -the supercharger is working and there is airflow through the pipes
    -Only water will be present in the tank
    -Heat transfer will only happen between the pipes and the coolant, not with the coolant and the rest of the pod
    -No leakages.
    -Lagrangian Approach
    -Radiation heat transfer will be neglected due to its small value.
    -ALL measurements will be in SI units unless specified.

Counter-Flow Heat Exchanger
"""


#Necessary modules
import math
import matplotlib.pyplot as plt


#Necessary variables:


t_sim = 600 # Total time for the simulation
t = range(0, t_sim) # Time

# Pipe Properties
r1 = 0.0045 # Inside radius of the pipe
r2 = 0.005375 # Outside radius of the pipe, WARNING: It is just an estimation
ID = 2*r1 # Inside Diameter of the pipe
OD = 2*r2 # Outside Diameter of the pipe
L = 18.0000# Length of the pipe
thick = r2 -r1 # Thickness of the wall
Area = L*2*math.pi*r1 # Inside Area of the pipe
g = 9.80000 # gravitational acceleration on Earth
m_water = 20.0000 # Total mass of water
m_air = 0.450000 # Mass flowrate of air, BIG ASSUMPTION ASSUMPTION
m_pipe = 8050.000*L*math.pi*((r2**2)-(r1**2)) # Mass of the pipe
vel = 10.0000 # Velocity of the air relative to the pod, BIG ASSUMPTION
travel_time = L/vel# Time that the air stays in the heat exchanger area

# Thermal properties
k = 18.00000 # Thermal conductivity for stainless steel
C_water = 4186.0000 # Specifc heat of water
C_v_air = 721 # Specific heat of air at constant volume
C_p_air = 1000.000 # Specific heat of air at constant pressure
C_steel = 490.000 #Specific heat of steel
k_water = 0.0260#0.599 # Thermal conductivity of the water (as it was in the USSR, the US has too many of them)
dyn_visco_water = 1.519 # Viscosity of the water
kin_visco_water = dyn_visco_water/1000.000 # Kinematic viscosity of water
B_water = 0.000044 # Coefficient of thermal expansion for water at 278K
Pr = (C_water*dyn_visco_water)/k_water # Prandtl number

# Thermal-fluid computations for air
j = m_air / Area # Mass flux accross pipe
u = 1.983 * (10**(-5)) # Dynamic viscosity of air
h_1 = (k /ID) * 0.023 * ((j * ID / u) ** 0.8) * ((u * C_p_air / k) ** 0.33) # Heat transfer coefficient for air and pipe

# Temperature arrays:
T_air = [] # Compressed air
T_water = [] # Liquid water
T_ia = 394.261 # Temperature of air after it exits the supercharger
T_iw = 273.000 # Initial water temperature in the heat exchanger
T_ip = 274.000 # Initial pipe temperature in the heat exchanger
T_pipe = 274.000 # Initial temperature of the pipe, to be updated
HT = [] # Heat transfer array


# Function time:

def Grashof(pipe, water): # Grashof Number
    # pipe: T of pipe
    # water: T of water
    Top = g*B_water*(pipe-water)*(OD**3)
    Down = kin_visco_water**2
    Gr = Top/Down
    return Gr # Computes the Grashof number

def Ra(pipe, water): # Rayleigh Number
    Ra = Grashof(pipe, water)*Pr
    return Ra

def h_2(pipe, water): # Heat transfer coefficient for water and pipe
    h_2 = (k/OD) * (0.6 + ((0.387*Ra(pipe,water) ** (1/6)) / (1 + (0.559/Pr) ** (9/16))**8.27)) ** 2
    return h_2

def U(pipe, water): # Overall heat transfer coefficient
    term2 = (r2 - r1) / k
    U = ((1 / h_1) + term2 + (1 / h_2(pipe, water))) ** (-1)
    return U


# Actual Heat Transfer

def Q_dot(T_A, T_W, T_pipe): # Heat Transfer
    # T_A (air, exit), T_W (cooling fluid, water for now)
    # D: Diameter of the pipe
    # L: Length of the pipe
    # U: overall heat transfer coefficient
    Q = -(U(T_pipe,T_W)*math.pi*OD*L)*((T_ia - T_A)/math.log((T_W-T_A)/(T_W-T_ia)))
    return Q


# The final Heat Transfer loop for 20 minutes (1200 s) of continued use

for qq in t:
    #Heat Transfer
    if t[qq] == 0: # First second
        HT.append(Q_dot(320.000, T_iw, T_ip)) # An arbitrary exit tem`perature of air needs to be chosen
    else: # Forever
        HT.append((Q_dot(T_air[qq-1], T_water[qq-1], T_pipe)))

    # Change of temperatures

    T_air.append(T_ia - ((HT[qq]*travel_time)/(m_air*C_v_air))) # Exhaust temperature of air
    if t[qq]==0: # For the first second, water
        T_water.append(T_iw + ((HT[qq])/(m_water*C_water)))
    else: # For the rst of time, water
        T_water.append(T_water[qq-1] + ((HT[qq])/(m_water*C_water)))
    T_pipe = T_pipe + ((HT[qq])/(m_pipe*C_steel)) # Updates the temperature of the pipe, it is a necessary assumption,
                # a necessary evil




# Plots stuff

# Temperature of fluids
fig, ax1 = plt.subplots()
ax1.plot(t, T_water, 'b-', label = 'Water') # Water
ax1.plot(t, T_air, 'k', label = 'Air, Exit') # Air
ax1.set_xlabel('Time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Temperature (K)', color='K')
for tl in ax1.get_yticklabels():
    tl.set_color('k')
plt.legend(bbox_to_anchor=(0.9, 0.40),bbox_transform=plt.gcf().transFigure) # Locates the legend

# Heat Transfer
ax2 = ax1.twinx() # Creates another y axis for Heat Transfer
ax2.plot(t, HT, 'r-', label = 'Heat Transfer')
ax2.set_ylabel('Heat Transfer (W)', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.legend(bbox_to_anchor=(0.9, 0.32), bbox_transform=plt.gcf().transFigure) # Locates the legend
plt.title('Water cooling, counter-flow; '+str(t_sim/60.00)+' min')
plt.show()
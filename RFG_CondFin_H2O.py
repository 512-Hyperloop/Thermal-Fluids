# Fall 2016
# 512 Hyperloop documentation
# Redondo, Carlos; Quartermaster, leader of piping sub-team
# Python 3.5.2

# Imports the necessary modules
import math
from enum import Enum
import matplotlib.pyplot as plt


# Classes

# Materials, Fluids, and Equipment

class Metal(Enum): # Stores the properties of metals we may use
    # Metal = (Density, Specific Heat, Thermal Conductivity)
    COPPER    = (8900.000, 385.00, 401.0)
    STEEL304  = (8000.000, 500.000, 16.2)

    def __init__(self, density, C, k): # Calls the properties
        self.density = density
        self.C = C
        self.k = k


class Silicon: # Silicon will be used as the de-fault electronic material
    den = 2329.000
    C = 700.000

    def __init__(self, Temperature):
        self.T = Temperature

    def k(self): # Computes the thermal conductivity, which varies with temperature
        k = 1.5*(((self.T)/300)**(-4/3))
        return k


class Water: # Stores the properties of the water
    den = 1000.000       # Density
    C = 4186.000         # Specific Heat
    k = 0.599            # Thermal conductivity
    Beta = 0.000044      # Expansion coefficient
    dyn_visco = 1.519E-3 # Dynamic viscosity
    kin_visco = 1.519E-6 # Kinematic viscosity

    Prandtl = (C*dyn_visco)/k # Prandtl number

    def __init__(self, Temperature): # Returns the temperature of the water
        self.T = Temperature

        if Temperature < 0: # Makes sure that the temperature of the water does not fall into a physical impossibility
            raise ValueError('Temperature of the water cannot be negative')



# Variables:

t_sim = 600# Time of the simulation

if t_sim <= 0: # Checks that the time of the simulation is, in fact, positive
    raise ValueError('There is no such thing as negative time in Heat Transfer')

t = range(0, int(t_sim)) # Steps of time in the simualtion
Fin_Mat = 304 # Material of the fin; 304 for Steel 304, 29 for Copper

if ((Fin_Mat == 304) or (Fin_Mat == 29)): # Makes sure that the material selected is inside the metal class
    pass
else:
    raise ValueError('Material properties not found')

# Electronics fin
L_elec = # Length
y_elec = # Width
z_elec = # Height
V_elec = L_elec * y_elec * z_elec  # Volume Volume
A_elec = L_elec * z_elec  # Cross-sectional Area
P_elec = 2*L_elec+ 2*z_elec # Cross-sectional perimeter
n_elec =  # Number of fins
# Supercharger fin
L_sup =
y_sup =
z_sup =
V_sup =
A_sup =
P_sup =
n_sup =

# Mechanics
g = 9.800  # Gravitational acceleration
# Thermal properties
H_elec = 100 # Total Heat dissipated by electronics
H_sup = # Total heat dissipated by the supercharger
T_ielec = # Initial temperature of electronics
T_isup =  # Initial temperature of the supercharger
T_iw = # Initial temperature of the water
m_elec = 3.00 # Mass of electronic equipment
m_sup = 9.07185 # Mass of the supercharger
# Thermal arrays
T_elec = []  # Temperature of electronics, cooled
T_sup = []   # Temperature of supercharger, cooled
UNT_elec = [] # Uncooled electronics
UNT_sup = [] # Uncooled supercharger
T_water = [] # Temperature of the water
HT_elec = [] # Heat transfer between electronics and water
HT_sup = []  # Heat transfer between supercharger and water


# Fluid computations and properties
R = 0.025  # Radius of the pipe
Nu_0 = 0.68 # Base Nusselt number
f_4 = (1 + (0.5/Water.Prandtl)**(9/16))**(-16/9)


# Function time

# Mathematical functions
def tan_h(x): # Hyperbolic tangent
    Top = 1 -math.e**(-2*x)
    Down = 1 +math.e**(-2*x)
    return Top/Down

# Thermal calculations
def Grashof (T_s, T_f, L): # Computes the Grashof number of the cooling fluid
    # T_s: Surface temperature of the fin
    # T_f: Surface temperature of the fluid
    # L is the length of the fin, which means that fin must be specified
    Top = g*Water.Beta*(T_s - T_f)*(L**3)
    Down = Water.kin_visco**2
    Gr_x = Top/Down
    return Gr_x

def Ra(T_s, T_f, L): # Defines the Rayleigh number for the fluid
    Ra = Grashof(T_s, T_f, L)*Water.Prandtl
    return Ra

def Nu(T_s, T_f, L): # Computes the Nusselt number
    Front = Nu_0**0.5
    Term2 = Ra(T_s, T_f, L)**(1/6)
    Term3 = (f_4/300)**(1/6)
    Nusselt = (Front + Term2*Term3)**2
    return Nusselt

def h_COPPER(T_s, T_f, L): # Computes the convective h between Copper fin and the water
    h = (Nu(T_s, T_f, L)*Metal.COPPER.k)/L_elec
    return h

def h_STEEL304(T_s, T_f, L): # Computes the h between Steel fin and the water
    h = (Nu(T_s, T_f, L)*Metal.STEEL304.k)/L_elec
    return h

# Heat transfer
def Q_elec(T_thing, T_f): # Between electronics and water

    if Fin_Mat == 304: # Fins made of 304 Stainless Steel
        m = Metal.STEEL304.density*V_elec
        k = Metal.STEEL304.k
        h = h_STEEL304(T_thing, T_f, L_elec) # Heat transfer coefficient
        Q_dot = n_elec*math.sqrt(k*A_elec*h*P_elec)*(T_thing-T_f)*tan_h(m*L_elec)

        return Q_dot

    elif Fin_Mat == 29: # Fins made of Copper
        m = Metal.COPPER.density * V_elec
        k = Metal.COPPER.k
        h = h_COPPER(T_thing, T_f, L_elec)  # Heat transfer coefficient
        Q_dot = n_elec * math.sqrt(k * A_elec * h * P_elec) * (T_thing - T_f) * tan_h(m * L_elec)

        return Q_dot



def Q_sup(T_thing, T_f): # Between supercharger and water

    if Fin_Mat == 304: # If the fins were made of Steel 304
        m = Metal.STEEL304.density*V_sup
        k = Metal.STEEL304.k
        h = h_STEEL304(T_thing, T_f, L_sup) # Heat transfer coefficient
        Q_dot = n_sup*math.sqrt(k*A_sup*h*P_sup)*(T_thing-T_f)*tan_h(m*L_sup)

        return Q_dot

    elif Fin_Mat == 29: # If the fin were made of Copper
        m = Metal.COPPER.density*V_sup
        k = Metal.COPPER.k
        h = h_COPPER(T_thing, T_f, L_sup) # Heat transfer coefficient
        Q_dot = n_sup*math.sqrt(k*A_sup*h*P_sup)*(T_thing-T_f)*tan_h(m*L_sup)

        return Q_dot



# Actual heat transfer computing

# For the uncooled

for qq in t:
    if t[qq] == 0: # For the first second
        UNT_elec.append(T_ielec)
        UNT_sup.append(T_isup)
    else: # For the rest of eternity
        UNT_elec.append(T_elec[qq] + H_elec/(m_elec*Silicon.C))
        UNT_sup.append(T_sup[qq] + H_sup/(m_sup*Metal.STEEL304.C))






# Plots stuff

fig = plt.figure(1) # Opens a new figure, the only one in this case
fig.suptitle('Thermal Analysis of SUpercharger and Electronics')

# Uncooled Electronics
plt.subplot(221)
plt.plot(t, UNT_elec, 'y-')
plt.title('Non-refrigerated electronics')
plt.xlabel('Time (s)')
plt.ylabel('T (k)')

# Uncooled  supercharger
plt.subplot(222)
plt.plot(t, UNT_sup, 'k-')
plt.title('Non-refrigerated supercharger')
plt.xlabel('Time (s)')
plt.ylabel('T (k)')

# Refrigerated Electronics

# Refrigerated Supercharger


# Constants: This will include all constants for the optimization

batteryCapacity = 100 # Watt hours
propulsionEfficiency = 0.75 # set as a constant but will be dynamic later
energyUsable = batteryCapacity * propulsionEfficiency * 3600 # joules
rho = 1.225 # kg/m^3
n_max = 8 # g's
CLmax = 1.6
g = 9.81 #m/s^2
CD0 = 0.03
straightDist = 304.8 # m
maxSpan = 1.524 # m 
minSpan = 0.9144
oswaldEff = 0.8

weightForBattery = batteryCapacity * 3600 / 500000 # kg    500,000 J / kg

# define a M2 and M3 (mass)

lp1 = 6
lp2 = 2
lc1 = 10
lc2 = 8
Ce = 10
Cp = 0.5
Cc = 2
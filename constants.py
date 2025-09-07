# Constants: This will include all constants for the optimization

duck_constraint = 250

batteryCapacity = 100 # Watt hours
propulsionEfficiency = 0.75 # set as a constant but will be dynamic later
energyUsable = batteryCapacity * propulsionEfficiency * 3600 # joules
rho = 1.225 # kg/m^3
n_max = 8 # g's
CLmax = 1.2
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

# --- Tail constants 
tail_VH      = 0.95   # your H-stab volume coefficient
tail_VV      = 0.10   # your V-stab volume coefficient
tailArmH     = 1.5    # m, horiz tail moment arm l_H (set to your fuselage length to tail AC)
tailArmV     = 1.5    # m, vert tail moment arm l_V (often ~ l_H)
Cfe_tail     = 0.006  # flat-plate equivalent for tail surfaces (0.005-0.008 typical)

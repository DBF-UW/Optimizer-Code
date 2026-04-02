# Constants: This will include all constants for the optimization
import aero_functions as aero

duck_constraint = 55

mu = 1.81e-5 # kg / (m * s)
mu_r = 0.04 # rolling friction coefficient

static_thrust = 72 # Newtons

batteryCapacity = 100 # Watt hours
propulsionEfficiency = 0.7 # set as a constant but will be dynamic later
energyUsable = batteryCapacity * propulsionEfficiency * 3600 # joules
rho = 1.225 # kg/m^3
n_max = 5.7 # 100 # g's
CLmax_takeoff = 0.6
CLmax = 1.1
g = 9.81 #m/s^2
CD0 = 0.03 # 0.06
inducedDragFactor = 1
straightDist = 304.8 # m
maxSpan = 1.524 # m 
minSpan = 0.9144
oswaldEff = 0.7

fus_drag_correction_factor = 2
fuselage_drag_factor = 1 # this could be tuned to 16 for accurate drag predictions ... 
# 2.4 will give you 80 break even

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

#volume parms

duck_length = 2.5 * 0.0254
duck_width = 2.3 * 0.0254
duck_height = 2.5 * 0.0254

puck_diameter = 0.0762
puck_thickness = 1 * 0.0254

# tunable 
PUCK_PACKING_COEFFICEINT = 1
FUSELAGE_PACKING_FACTOR = 1
stuctures_correction_factor = 1.1
banner_turn_drag_factor = 2
fuse_weight_correction_factor = 4.84

carbon_fiber_density = 0.088 # kg / m^2
nomex_density = 0.058 # kg / m^2

zero_lift_correction_factor = 2.38

lap_breakdown = 20 # break the straights into x segments
lap_breakdown_turn = 8 # break the turns into x segments

initial_height = 0

load_voltage = 22.2
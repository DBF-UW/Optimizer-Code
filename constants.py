"""
Stores all useful constants

Resources
---------
Pink Foam Density
    https://www.homedepot.com/p/Owens-Corning-FOAMULAR-150-2-in-x-4-ft-x-8-ft-R-10-Scored-Squared-Edge-Rigid-Foam-Board-Insulation-Sheathing-45W/100320352
"""

# =========== PHYSICAL CONSTANTS ===========
GRAVITATIONAL_ACCELERATION = 9.80665  # m/s^2
EARTH_RADIUS = 6371e3  # meters
R = 287.05  # J/(kg*K) gas constant for dry air
PS = 101325  # Pa standard pressure
RHOS = 1.225  # kg/m^3 standard density
TS = 288.15  # K standard temperature
SPECIFIC_HEAT_AIR_CONSTANT_PRESSURE = 1004  # J/(kg*K)
SPECIFIC_HEAT_AIR_CONSTANT_VOLUME = 717  # J/(kg*K)

# =========== ENVIROMENTAL CONSTANTS ========
RHO = 0.0021 # slug/ft3
T = 72.3238 # F
MU_ROLL = 0.05 # unitless

# =========== MATERIAL CONSTANTS ===========
PINK_FOAM_DENSITY = 23.637083912 # kg/m^3
LOAD_FACTOR_LIMIT = 8 # g's

# =========== A&P CONSTANTS ============
PROPULSION_EFFICIENCY = 0.75 # unitless
BATTERY_ENERGY = 100  # Wh/kg
MOTOR_MASS = 0.5  # kg
LG_MASS = 0.5  # kg
BATTERY_SPECIFIC_ENERGY = 500000 # Wh/kg
# =========== STRUCTURAL CONSTANTS ========
STRUCTURAL_SAFETY_FACTOR = 1.5  # unitless
WING_SURFACE_DENSITY = 2  # kg/m^2
# =========== 2024-2025 DBF REQS ===========
AIAA_LENGTH = 1000 # ft

MAX_WING_SPAN = 5 # ft
MIN_WING_SPAN = 3 # ft
# Mission 1
MISSION_1_TIME = 600
MISSION_1_POINTS = 1

# Mission 2
MISSION_2_TIME = 600
MISSION_2_POINTS = 1
LP1 = 6
LP2 = 2
LC1 = 10
LC2 = 8
CE = 10
CP = 0.5
CC = 2
EF = 1
PASSENGER_MASS = 0.02 # N
CARGO_MASS = 0.170 # N

# Mission 3
MISSION_3_TIME = 300 #Seconds
MISSION_3_POINTS = 2




# =========== VLM CONSTANTSs ===========
SPAN_RESOLUTION = 8
CHORD_RESOLUTION = 6
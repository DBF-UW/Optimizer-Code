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
STATIC_THRUST = 70 # N
DYNAMIC_THRUST = lambda v: (-0.0258631 * v * v) + (0.916509 * v) + 97.452 # N <- This is a curve fit from 23-24 data (Data provided from Josh)

# =========== 2024-2025 DBF REQS ===========
AIAA_LENGTH = 1000 # ft

MAX_WING_SPAN = 5 # ft
#MIN_FUEL_TANKS = 2

#MAX_X1_WEIGHT = 0.55 # lb
#MIN_X1_RELEASE = 200 # ft
#MAX_X1_RELEASE = 400 # ft

# Mission 1
MISSION_1_TIME = 600
MISSION_1_POINTS = 1

# Mission 2
MISSION_2_TIME = 600
#MISSION_2_LAPS = 3
MISSION_2_POINTS = 1
LP1 = 6
LP2 = 2
LC1 = 10
LC2 = 8
CE = 10
CP = 0.5
CC = 2
EF = 1
PASSENGER_WEIGHT = 0.1946096957 # N
CARGO_WEIGHT = 1.9460969567 # N

# Mission 3
MISSION_3_TIME = 600
MISSION_3_POINTS = 2




# =========== VLM CONSTANTSs ===========
SPAN_RESOLUTION = 8
CHORCH_RESOLUTION = 6
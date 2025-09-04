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
RHO = 1.225  # kg/m^3 standard density
MEW = 1.802 * 10**-5 #kg/m*s dynamic viscosity
TS = 288.15  # K standard temperature
SPECIFIC_HEAT_AIR_CONSTANT_PRESSURE = 1004  # J/(kg*K)
SPECIFIC_HEAT_AIR_CONSTANT_VOLUME = 717  # J/(kg*K)

# =========== ENVIROMENTAL CONSTANTS ========

# =========== MATERIAL CONSTANTS ===========
PINK_FOAM_DENSITY = 23.637083912 # kg/m^3
LOAD_FACTOR_LIMIT = 8 # g's

# =========== A&P CONSTANTS ============
PROPULSION_EFFICIENCY = 0.75 # unitless
BATTERY_ENERGY = 100  # Wh
MOTOR_MASS = 0.5  # kg
LG_MASS = 0.5  # kg
BATTERY_SPECIFIC_ENERGY = 178000 # Wh/kg

# =========== Mission Constants ===========
PASSENGER_INCOME_FIXED = 6  # $/passenger
PASSENGER_INCOME_LAP = 2  # $/passenger/lap
CARGO_INCOME_FIXED = 10  # $/cargo
CARGO_INCOME_LAP = 8  # $/cargo/lap
BASE_OPERATING_COST = 10  # $/lap
PER_PASSENGER_COST = 0.5  # $/passenger/lap
PER_CARGO_COST = 2  # $/cargo/lap

DUCK_WIDTH = 0.0584 #meters
DUCK_HEIGHT =  0.0635 #meters
DUCK_LENGTH = 0.0635 #meters

PUCK_THICKNESS = 0.0254 #meters
PUCK_DIAMETER = 0.0762 #meters
PUCK_PACKING_COEFFICEINT = 0.65 #unitless

PASSENGER_MASS = 0.02 + 0.01# KG
CARGO_MASS = 0.170 # KG
# =========== STRUCTURAL CONSTANTS ========
STRUCTURAL_SAFETY_FACTOR = 1.5  # unitless
WING_SURFACE_DENSITY = 2  # kg/m^2

CARBON_FIBER_DENSITY = 0.088 #kg/m^2
NOMEX_DENSITY = 0.058 #kg/m^2
GOOP_MODIFIER = 1.12

BANNER_SURFACE_DENSITY = 0.075 #kg/m^2

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



# Mission 3
MISSION_3_TIME = 300 #Seconds
MISSION_3_POINTS = 2

# =========== VLM CONSTANTSs ===========
SPAN_RESOLUTION = 8
CHORD_RESOLUTION = 6